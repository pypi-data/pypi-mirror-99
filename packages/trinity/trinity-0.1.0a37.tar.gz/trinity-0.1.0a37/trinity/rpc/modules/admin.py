
from typing import Tuple, Iterable, Dict, Sequence

from eth.constants import GENESIS_BLOCK_NUMBER
from eth_typing import BlockNumber
from eth_utils import encode_hex, to_dict

from lahja import EndpointAPI

from p2p.disconnect import DisconnectReason
from p2p.kademlia import Node
from p2p.typing import Capabilities
from p2p.validation import validate_enode_uri

from trinity.chains.base import AsyncChainAPI
from trinity.config import TrinityConfig, Eth1AppConfig, Eth1ChainConfig
from trinity.constants import TO_NETWORKING_BROADCAST_CONFIG
from trinity.protocol.common.events import (
    ConnectToNodeCommand,
    DisconnectFromPeerCommand,
    GetConnectedPeersRequest,
    GetProtocolCapabilitiesRequest,
    PeerInfo,
)
from trinity.rpc.modules import Eth1ChainRPCModule
from trinity.rpc.typing import RpcProtocolResponse, RpcNodeInfoResponse
from trinity.server import BOUND_IP
from trinity.rpc.typing import RpcPeerResponse
from trinity._utils.version import construct_trinity_client_identifier


def format_enode(config: TrinityConfig) -> str:
    return f"enode://{config.nodekey.public_key.to_hex()[2:]}@{BOUND_IP}:{config.port}"


@to_dict
def generate_chain_config(chain_config: Eth1ChainConfig) -> Iterable[Tuple[str, int]]:
    for fork_block, vm in chain_config.vm_configuration:
        yield f"{vm.fork}Block", fork_block

    yield 'chainId', chain_config.chain_id


class Admin(Eth1ChainRPCModule):

    def __init__(self,
                 chain: AsyncChainAPI,
                 event_bus: EndpointAPI,
                 trinity_config: TrinityConfig) -> None:
        super().__init__(chain, event_bus)
        self.trinity_config = trinity_config

    async def addPeer(self, uri: str) -> None:
        validate_enode_uri(uri, require_ip=True)

        await self.event_bus.broadcast(
            ConnectToNodeCommand(Node.from_uri(uri)),
            TO_NETWORKING_BROADCAST_CONFIG
        )

    async def removePeer(self, uri: str) -> bool:
        validate_enode_uri(uri, require_ip=True)
        peer_to_remove = Node.from_uri(uri)

        response = await self.event_bus.request(GetConnectedPeersRequest())
        for connected_peer_info in response.peers:
            if peer_to_remove == connected_peer_info.session.remote:
                await self.event_bus.broadcast(
                    DisconnectFromPeerCommand(
                        connected_peer_info,
                        DisconnectReason.DISCONNECT_REQUESTED,
                    ),
                )
                return True
        return False

    async def nodeInfo(self) -> RpcNodeInfoResponse:
        response = await self.event_bus.request(
            GetProtocolCapabilitiesRequest(),
            TO_NETWORKING_BROADCAST_CONFIG
        )
        return {
            'enode': format_enode(self.trinity_config),
            # TODO: get the external ip from the upnp service
            'ip': "::",
            'listenAddr': f"[::]:{self.trinity_config.port}",
            'name': construct_trinity_client_identifier(),
            'ports': {
                'discovery': self.trinity_config.port,
                'listener': self.trinity_config.port
            },
            'protocols': await self._generate_protocol_info(response.capabilities)
        }

    async def _generate_protocol_info(
            self,
            protocols: Capabilities) -> Dict[str, RpcProtocolResponse]:

        head = await self.chain.coro_get_canonical_head()
        total_difficulty = await self.chain.coro_get_score(head.hash)
        genesis_header = await self.chain.coro_get_canonical_block_header_by_number(
            BlockNumber(GENESIS_BLOCK_NUMBER)
        )
        chain_config = self.trinity_config.get_app_config(Eth1AppConfig).get_chain_config()

        return {
            protocol: {
                'version': f'{protocol}/{version}',
                'difficulty': total_difficulty,
                'genesis': encode_hex(genesis_header.hash),
                'head': encode_hex(head.hash),
                'network': self.trinity_config.network_id,
                'config': generate_chain_config(chain_config)
            }
            for protocol, version in protocols
        }

    def _format_peer(self, peer_info: PeerInfo) -> RpcPeerResponse:
        session = peer_info.session
        return {
            'enode': session.remote.uri(),
            'id': str(session.id),
            'name': peer_info.client_version_string,
            'caps': [f"{protocol}/{version}" for protocol, version in peer_info.capabilities],
            'network': {
                'localAddress': f"{BOUND_IP}:{self.trinity_config.port}",
                'remoteAddress': f"{session.remote.address.ip}:{session.remote.address.tcp_port}",
                'inbound': peer_info.inbound
            }
        }

    async def peers(self) -> Sequence[RpcPeerResponse]:

        response = await self.event_bus.request(GetConnectedPeersRequest())

        return tuple(
            self._format_peer(peer_info)
            for peer_info in response.peers
        )

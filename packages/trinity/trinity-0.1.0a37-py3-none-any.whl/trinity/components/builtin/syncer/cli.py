import argparse
import os
from pathlib import PurePosixPath
import re
import urllib
from typing import (
    Any,
    Dict,
)

from eth.consensus.clique.constants import (
    EPOCH_LENGTH
)

from eth_typing import (
    Hash32,
    HexStr,
)

from eth_utils import (
    decode_hex,
    is_hex,
    to_int,
    remove_0x_prefix,
    ValidationError,
)

from trinity.network_configurations import (
    MiningMethod,
    PRECONFIGURED_NETWORKS,
)

from trinity.sync.common.checkpoint import Checkpoint

from .etherscan_api import (
    Etherscan,
    Network,
)


def is_block_hash(value: str) -> bool:
    return is_hex(value) and len(remove_0x_prefix(HexStr(value))) == 64


def remove_non_digits(value: str) -> str:
    return re.sub(r"\D", "", value)


def get_latest_clique_checkpoint_block_number(latest_block_number: int) -> int:
    if EPOCH_LENGTH > 0:
        for block_number in range(latest_block_number, 0, -1):
            if block_number % EPOCH_LENGTH == 0:
                return block_number

    return latest_block_number


def parse_checkpoint_uri(uri: str, network_id: int) -> Checkpoint:
    try:
        parsed = urllib.parse.urlparse(uri)
    except ValueError as e:
        raise ValidationError(str(e))

    path = parsed.path.lower()
    if path.startswith('/byhash'):
        return parse_byhash_uri(parsed)
    elif path == '/byetherscan/latest':
        return parse_byetherscan_uri(parsed, network_id)
    else:
        raise ValidationError("Not a valid checkpoint URI")


BLOCKS_FROM_TIP = 5000


def get_checkpoint_block_byetherscan(network_id: int) -> Dict[str, Any]:
    try:
        network = Network(network_id)
    except ValueError:
        raise ValidationError(
            f"Can not resolve checkpoint through Etherscan API"
            f"for network {network_id}. Network not supported"
        )

    try:
        etherscan_api_key = os.environ['TRINITY_ETHERSCAN_API_KEY']
    except KeyError:
        raise RuntimeError(
            "Etherscan API key missing. Assign your Etherscan API key "
            "to the TRINITY_ETHERSCAN_API_KEY environment variable."
        )

    etherscan_api = Etherscan(etherscan_api_key)

    latest_block_number = etherscan_api.get_latest_block(network)

    if PRECONFIGURED_NETWORKS[network_id].mining_method == MiningMethod.Clique:
        checkpoint_block_number = get_latest_clique_checkpoint_block_number(
            latest_block_number - BLOCKS_FROM_TIP,
        )
    else:
        checkpoint_block_number = latest_block_number - BLOCKS_FROM_TIP

    return etherscan_api.get_block_by_number(checkpoint_block_number, network)


def parse_byetherscan_uri(parsed: urllib.parse.ParseResult, network_id: int) -> Checkpoint:
    checkpoint_block_response = get_checkpoint_block_byetherscan(network_id)

    checkpoint_score = to_int(hexstr=checkpoint_block_response['totalDifficulty'])
    checkpoint_hash = checkpoint_block_response['hash']

    return Checkpoint(Hash32(decode_hex(checkpoint_hash)), checkpoint_score)


def parse_byhash_uri(parsed: urllib.parse.ParseResult) -> Checkpoint:
    scheme, netloc, query = parsed.scheme, parsed.netloc, parsed.query

    try:
        parsed_query = urllib.parse.parse_qsl(query)
    except ValueError as e:
        raise ValidationError(str(e))

    query_dict = dict(parsed_query)

    # we allow any kind of separator for a nicer UX. e.g. instead of "11487662456884849810705"
    # one can use "114 876 624 568 848 498 107 05" or "1,487,662,456,884,849,810,705". This also
    # allows copying out a value from e.g etherscan.
    score = remove_non_digits(query_dict.get('score', ''))

    parts = PurePosixPath(parsed.path).parts

    if len(parts) != 3 or scheme != 'eth' or netloc != 'block' or not score:
        raise ValidationError(
            'checkpoint string must be of the form'
            '"eth://block/byhash/<hash>?score=<score>"'
        )

    block_hash = parts[2]

    if not is_block_hash(block_hash):
        raise ValidationError(f'Block hash must be valid hex string, got: {block_hash}')

    if not score.isdigit():
        raise ValidationError(f'Score (total difficulty) must be an integer, got: {score}')

    return Checkpoint(Hash32(decode_hex(block_hash)), int(score))


class NormalizeCheckpointURI(argparse.Action):
    """
    Normalize the URI describing a sync checkpoint.
    """
    def __call__(self,
                 parser: argparse.ArgumentParser,
                 namespace: argparse.Namespace,
                 value: Any,
                 option_string: str = None) -> None:

        try:
            parsed = parse_checkpoint_uri(value, namespace.network_id)
        except (ValidationError, RuntimeError) as exc:
            raise argparse.ArgumentError(self, str(exc))
        setattr(namespace, self.dest, parsed)

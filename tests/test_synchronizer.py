from decimal import Decimal
from datetime import datetime, timezone

from app.events_syncronizer import DistributionEventsSynchronizer
from app.models import Distribution
from config import ETH_RPC, CONTRACT_ADDRESS


def test_synchronizer(drop_tables, session, mocker):
    """
    Checks distribution on 28.12.2023 (7 events)
    """

    mocker.patch('app.events_syncronizer.INITIAL_BLOCK', 18880873)

    s = DistributionEventsSynchronizer(ETH_RPC, CONTRACT_ADDRESS)
    date = datetime(2023, 12, 28, tzinfo=timezone.utc)

    s.sync(18886097)  # 5 events

    assert session.query(Distribution).count() == 5

    def round_decimals(d, pr=16):
        return {
            k: round(v, pr) if isinstance(v, Decimal) else v for k, v in d.items()
        }

    test_stat = {
        'total_input_aix': Decimal(sum([
            5675514270875124469698, 5182281517621412568093, 5174284867714587043687,
            5269404430913916281648, 5622437480660180911370
        ])) / Decimal(1e18),
        'total_distributed_aix': Decimal(0),
        'total_swapped_eth': Decimal(sum([
            572534889168040907, 501093531600099907, 482654845386659653, 484993754552426048, 474758569715013283
        ])) / Decimal(1e18),
        'total_distributed_eth': (Decimal(sum([
            572534889168040907, 501093531600099907, 482654845386659653, 484993754552426048, 474758569715013283
        ])) / Decimal(1e18)),
        'distributors': [
            '0x9A0A9594Aa626EE911207DC001f535c9eb590b34'
        ],
        'first_ts': datetime(2023, 12, 28, 1, 34, 11),
        'last_ts': datetime(2023, 12, 28, 19, 11, 11)
    }
    assert round_decimals(Distribution.get_day_statistic(date)) == round_decimals(test_stat)

    # +2 event
    test_stat['total_input_aix'] += Decimal(5009644381003376377109 + 5397538783108195157256) / Decimal(1e18)
    test_stat['total_swapped_eth'] += Decimal(435739889055924225 + 485502243331771166) / Decimal(1e18)
    test_stat['total_distributed_eth'] += Decimal(435739889055924225 + 485502243331771166) / Decimal(1e18)
    test_stat['last_ts'] = datetime(2023, 12, 28, 23, 35, 35)

    # check checkpoint local
    s.sync(18887414)
    assert session.query(Distribution).count() == 7
    assert round_decimals(Distribution.get_day_statistic(date)) == round_decimals(test_stat)

    # check checkpoint db
    (
        session
        .query(Distribution)
        .filter(Distribution.block.in_([18887413, 18886508]))
        .delete()

    )
    session.commit()
    assert session.query(Distribution).count() == 5

    s = DistributionEventsSynchronizer(ETH_RPC, CONTRACT_ADDRESS)
    s.sync(18887414)
    assert session.query(Distribution).count() == 7
    assert round_decimals(Distribution.get_day_statistic(date)) == round_decimals(test_stat)

from datetime import datetime

from sqlalchemy import BigInteger, Column, String, DateTime, Numeric, func

from db.sessions import db_session
from .base import Model


class Distribution(Model):
    __tablename__ = 'distribution'

    id = Column(BigInteger, primary_key=True)
    block = Column(BigInteger, index=True, nullable=False)
    transaction = Column(String(66), index=True, nullable=False)
    sender = Column(String(42), index=True, nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)

    input_aix = Column(Numeric, nullable=False)
    distributed_aix = Column(Numeric, nullable=False)
    swapped_eth = Column(Numeric, nullable=False)
    distributed_eth = Column(Numeric, nullable=False)

    @classmethod
    def get_day_statistic(cls, date: datetime.date) -> dict:
        """
        Returns A dictionary containing the following statistics for the given date
        :param date: the date for which the statistics are calculated
        """
        start_of_day = datetime.combine(date, datetime.min.time())
        end_of_day = datetime.combine(date, datetime.max.time())

        with db_session() as session:
            stat = (
                session.query(
                    func.sum(cls.input_aix / 1e18).label("total_input_aix"),
                    func.sum(cls.distributed_aix / 1e18).label("total_distributed_aix"),
                    func.sum(cls.swapped_eth / 1e18).label("total_swapped_eth"),
                    func.sum(cls.distributed_eth / 1e18).label("total_distributed_eth"),
                    func.min(cls.timestamp).label("first_ts"),
                    func.max(cls.timestamp).label("last_ts"),
                )
                .filter(
                    cls.timestamp.between(start_of_day, end_of_day),
                )
                .first()
                ._asdict()
            )

            distributors = (
                session.query(
                    cls.sender
                )
                .filter(
                    cls.timestamp.between(start_of_day, end_of_day),
                )
                .distinct()
            )

            stat['distributors'] = [d[0] for d in distributors]
            return stat

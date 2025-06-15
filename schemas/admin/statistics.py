from datetime import date

from pydantic import BaseModel, Field

from enums.statistics import StatisticsIntervalEnum


class StatisticsPeriodSchema(BaseModel):
    date: str = Field(default=..., description="Period date (format: YYYY-MM-DD)")
    orders_count: int = Field(default=..., description="Number of orders in the period")
    new_clients_count: int = Field(
        default=..., description="Number of new clients in the period"
    )
    avg_order_price: float = Field(
        default=..., description="Average order price in the period"
    )
    avg_order_time: float = Field(
        default=..., description="Average order processing time in seconds"
    )


class StatisticsTotalsSchema(BaseModel):
    orders_count: int = Field(default=..., description="Number of orders in the period")
    new_clients_count: int = Field(
        default=..., description="Number of new clients in the period"
    )
    avg_order_price: float = Field(
        default=..., description="Average order price overall"
    )
    avg_order_time: float = Field(
        default=..., description="Average order processing time in seconds overall"
    )


class StatisticsFilterSchema(BaseModel):
    start_date: date = Field(default=..., description="Start date for statistics")
    end_date: date = Field(default=..., description="End date for statistics")
    interval: StatisticsIntervalEnum = Field(
        default=StatisticsIntervalEnum.DAILY,
        description="Interval for data aggregation (daily, weekly, monthly)",
    )


class StatisticsResponseSchema(BaseModel):
    date_min: str = Field(default=..., description="Minimum date for the statistics")
    date_max: str = Field(default=..., description="Maximum date for the statistics")
    totals: StatisticsTotalsSchema = Field(
        default=...,
        description="Total numbers for various statistics",
    )
    periods: list[StatisticsPeriodSchema] = Field(
        default=..., description="Periods with statistics"
    )
    interval: StatisticsIntervalEnum = Field(
        default=StatisticsIntervalEnum.DAILY,
        description="Interval for data aggregation (daily, weekly, monthly)",
    )

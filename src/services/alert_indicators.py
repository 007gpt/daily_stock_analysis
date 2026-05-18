# -*- coding: utf-8 -*-
"""Shared technical indicator helpers for reports and alert rules."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd


def calculate_wilder_rsi(close: pd.Series, period: int) -> pd.Series:
    """Calculate RSI with Wilder's EMA/SMMA smoothing."""
    if period <= 0:
        raise ValueError("period must be > 0")

    close_series = pd.Series(close, copy=False)
    delta = close_series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.ewm(alpha=1 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, adjust=False).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi.fillna(50)


def calculate_rsi(close: pd.Series, period: int) -> pd.Series:
    """Backward-compatible alias for the project RSI implementation."""
    return calculate_wilder_rsi(close, period)


def add_rsi_columns(
    df: pd.DataFrame,
    periods: Iterable[int],
    *,
    price_column: str = "close",
    column_prefix: str = "RSI",
) -> pd.DataFrame:
    """Return a copy of ``df`` with Wilder RSI columns for each period."""
    result = df.copy()
    for period in periods:
        result[f"{column_prefix}_{period}"] = calculate_wilder_rsi(result[price_column], int(period))
    return result

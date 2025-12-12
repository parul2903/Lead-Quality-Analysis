# src/sql_queries.py

# ---------------------------------------------------------
# Monthly Trend
# ---------------------------------------------------------
MONTHLY_TREND = """
SELECT
    Month,
    COUNT(*) AS total_leads,
    AVG(GoodLeadFlag) AS good_rate,
    AVG(BadLeadFlag) AS bad_rate,
    AVG(ClosedFlag) AS closed_rate
FROM leads
GROUP BY Month
ORDER BY Month;
"""

# ---------------------------------------------------------
# Widget Performance
# ---------------------------------------------------------
WIDGET_PERFORMANCE = """
SELECT
    WidgetName,
    COUNT(*) AS leads,
    AVG(GoodLeadFlag) AS good_rate,
    AVG(ClosedFlag) AS closed_rate,
    AVG(BadLeadFlag) AS bad_rate
FROM leads
GROUP BY WidgetName
ORDER BY good_rate DESC;
"""

# ---------------------------------------------------------
# Partner Performance
# ---------------------------------------------------------
PARTNER_PERFORMANCE = """
SELECT
    Partner,
    COUNT(*) AS leads,
    AVG(GoodLeadFlag) AS good_rate,
    AVG(BadLeadFlag) AS bad_rate,
    AVG(ClosedFlag) AS closed_rate
FROM leads
GROUP BY Partner
HAVING COUNT(*) > 10
ORDER BY good_rate DESC;
"""

# ---------------------------------------------------------
# Funnel Progression
# ---------------------------------------------------------
FUNNEL_STATUS = """
SELECT
    CallStatus,
    COUNT(*) AS leads,
    AVG(GoodLeadFlag) AS good_rate,
    AVG(ClosedFlag) AS closed_rate
FROM leads
GROUP BY CallStatus
ORDER BY leads DESC;
"""

# ---------------------------------------------------------
# Widget x Partner Cross Performance
# ---------------------------------------------------------
WIDGET_PARTNER_CROSS = """
SELECT
    WidgetName,
    Partner,
    COUNT(*) AS leads,
    AVG(GoodLeadFlag) AS good_rate
FROM leads
GROUP BY WidgetName, Partner
HAVING COUNT(*) > 8
ORDER BY good_rate DESC;
"""

# ---------------------------------------------------------
# Debt Level Quality
# ---------------------------------------------------------
DEBTLEVEL_PERFORMANCE = """
SELECT
    DebtLevel,
    COUNT(*) AS leads,
    AVG(GoodLeadFlag) AS good_rate,
    AVG(ClosedFlag) AS closed_rate
FROM leads
GROUP BY DebtLevel
ORDER BY good_rate DESC;
"""

# ---------------------------------------------------------
# Contactability Matrix
# ---------------------------------------------------------
CONTACTABILITY_MATRIX = """
SELECT
    PhoneBucket,
    AddressBucket,
    COUNT(*) AS leads,
    AVG(GoodLeadFlag) AS good_rate,
    AVG(ClosedFlag) AS closed_rate
FROM leads
GROUP BY PhoneBucket, AddressBucket
ORDER BY PhoneBucket, AddressBucket;
"""

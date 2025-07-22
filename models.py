from sqlalchemy import Table, Column, String, MetaData

metadata = MetaData()

urls = Table(
    "urls",
    metadata,
    Column("short_code", String, primary_key=True),
    Column("original_url", String, nullable=False),
)

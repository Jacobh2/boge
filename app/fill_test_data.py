from deps import get_db
from random import randint
from tqdm import tqdm
from datetime import datetime

db = get_db()


datapoints = 60 * 24 * 365 // 5


def get_date(index):
    return datetime.fromtimestamp(1672527600 + (300 * index))


for i in tqdm(range(datapoints)):
    query = """
        INSERT INTO sensor (name, value, src_created_at)
        VALUES (?, ?, ?);
    """
    for v in range(10):
        db.conn.execute(query, (f"temp_{v}", randint(190, 250) / 10, get_date(i)))

    if i % 1000 == 0:
        db.conn.commit()

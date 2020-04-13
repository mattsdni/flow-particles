# Flow Particle Demo


create rectangular grid in qgis with MMQGIS plugin

map mesh data onto grid with this sql query

```sql
update square_grid s set dx = sq.dx, dy = sq.dy
from
(select g.ogc_fid, g.wkb_geometry, sum(m.flow_velocity * cos(m.flow_angle * pi() / 180)) as dx, sum(m.flow_velocity * sin(m.flow_angle * pi() / 180)) as dy
from hazard_damages_1yvrjj9uwam3sr3bhhvbuolvsbp m
join square_grid g
on st_intersects(g.wkb_geometry, m.geometry)
group by g.ogc_fid) sq
where s.ogc_fid = sq.ogc_fid;
```

generate json data with python script
```python
import psycopg2
import json

DB_STRING = (
    "dbname='postgres' user='postgres' host='localhost' port='5438' password='password'"
)
conn = psycopg2.connect(DB_STRING)
cur = conn.cursor()


def generate():
    x = 0
    y = 0
    r = 10
    vel = []
    for j in range(0, 88):
        tmp_row = []
        for i in range(1, 101):
            id = i * 88 - j
            q = "select dx, dy from square_grid where ogc_fid = {}".format(id)
            cur.execute(q)
            conn.commit()
            row = cur.fetchone()
            tmp_row.append(
                {
                    "x": x * r,
                    "y": y * r,
                    "r": r,
                    "col": x,
                    "row": y,
                    "xv": 0 if row[0] is None else row[0],
                    "yv": 0 if row[1] is None else row[1],
                    "pressure": 0,
                }
            )
            y += 1
        x += 1
        y = 0
        vel.append(tmp_row)

    # fill in missing data with zeros
    for i in range(88, 101):
        tmp_row = []
        for j in range(1,101):
            tmp_row.append(
                {
                    "x": x * r,
                    "y": y * r,
                    "r": r,
                    "col": x,
                    "row": y,
                    "xv": 0,
                    "yv": 0,
                    "pressure": 0,
                }
            )
            y += 1
        x += 1
        y = 0
        vel.append(tmp_row)
    f = open('vel_dump3.js', 'w')
    f.write(json.dumps(vel))


if __name__ == "__main__":
    generate()

```

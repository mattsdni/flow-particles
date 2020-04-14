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
    width = 100
    height = 100
    starting_id = 114
    loop_count = 0
    vel = []
    for j in reversed(range(starting_id-height, starting_id+1)):
        tmp_row = []
        for i in range(1, width+1):
            id = i * starting_id - loop_count
            q = "select dx, dy from square_grid_hex2 where ogc_fid = {}".format(id)
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
                    "xv": 0 if row[0] is None else row[0]*10,
                    "yv": 0 if row[1] is None else row[1]*10,
                    "pressure": 0,
                }
            )
            y += 1
        x += 1
        y = 0
        vel.append(tmp_row)
        loop_count += 1

    # fill in missing data with zeros
    # for i in range(88, 101):
    #     tmp_row = []
    #     for j in range(1,101):
    #         tmp_row.append(
    #             {
    #                 "x": x * r,
    #                 "y": y * r,
    #                 "r": r,
    #                 "col": x,
    #                 "row": y,
    #                 "xv": 0,
    #                 "yv": 0,
    #                 "pressure": 0,
    #             }
    #         )
    #         y += 1
    #     x += 1
    #     y = 0
    #     vel.append(tmp_row)
    f = open('vel_dump7.js', 'w')
    f.write(json.dumps(vel))


if __name__ == "__main__":
    generate()

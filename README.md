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

#usage="rx.ll lidar_data.lle"
vertical_resolution=0.1
#echo "usage: $usage"
#echo ""
I="-I0.000004504504504504505"
rx_ll="rx.ll"
lidar_lle="lidar_data.lle"
output_lle="output.lle"

#get the boundaries of the lidar data
echo "minmax $I $lidar_lle"
echo ""
R=`minmax $I $lidar_lle`

#blockmedian filter the lidar data
echo "blockmedian $R $I $lidar_lle > temp.lle"
echo ""
blockmedian $R $I $lidar_lle > temp.lle

#remove old lidar_topo.grd file
echo "rm lidar_topo.grd"
echo ""
rm lidar_topo.grd

#
G="-Glidar_topo.grd"
echo "surface temp.lle $R $I $G"
echo ""
surface temp.lle $R $I $G


echo "makecpt -Ctopo `minmax -T${vertical_resolution}/2 temp.lle` -Z > colour.cpt"
echo ""
makecpt -Ctopo `minmax -T${vertical_resolution}/2 temp.lle` -Z > colour.cpt

echo "grdimage lidar_topo.grd -Ccolour.cpt
    $R
    -Jm750 -B0.005f0.0025g0.0025/0.0025f0.00175g0.00175nSeW
    -P  > lidar_topo.ps"
echo ""
grdimage lidar_topo.grd -Ccolour.cpt $R -Jm750 -B0.005f0.0025g0.0025/0.0025f0.00175g0.00175nSeW -P  > lidar_topo.ps

R=`minmax $I rx.ll`
echo "grdimage lidar_topo.grd -Ccolour.cpt $R\
    -Jm1500 -B0.005f0.0025g0.0025/0.0025f0.00175g0.00175nSeW -P\
    > lidar_topo.ps"
grdimage lidar_topo.grd -Ccolour.cpt $R -Jm1500 -B0.005f0.0025g0.0025/0.0025f0.00175g0.00175nSeW -P  > lidar_topo_zoom.ps

echo "rm temp.lle"
echo ""
rm temp.lle

echo "grdtrack $rx_ll $G > $output_lle"
echo ""
grdtrack $rx_ll $G > $output_lle

I="-I0.000004504504504504505"
echo "minmax $I $output_lle"
echo ""
R=`minmax $I $output_lle`
G="-Goutput_topo.grd"
echo "surface $output_lle $R $I $G"
echo ""
surface $output_lle $R $I $G
echo "minmax -T${vertical_resolution}/2 $output_lle"
echo ""
T=`minmax -T${vertical_resolution}/2 $output_lle`
echo "rm colour.cpt"
echo ""
rm colour.cpt
echo "makecpt -Ctopo $T -Z > colour.cpt"
echo ""
makecpt -Ctopo $T -Z > colour.cpt
echo "grdimage output_topo.grd -Ccolour.cpt $R -Jm1000 -P > plot.ps"
echo ""
grdimage output_topo.grd -Ccolour.cpt $R -Jm1000 -P > plot.ps
echo "gs -sDEVICE=x11 plot.ps"
echo ""
gs -sDEVICE=x11 plot.ps

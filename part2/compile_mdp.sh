python3 part2.py
file=pulak
/media/psf/Home/Desktop/Sem4/MDL/sarsop/src/pomdpconvert $file.pomdp
/media/psf/Home/Desktop/Sem4/MDL/sarsop/src/pomdpsol $file.pomdpx
/media/psf/Home/Desktop/Sem4/MDL/sarsop/src/pomdpeval --policy-file out.policy  --simLen 100 --simNum 100 $file.pomdp

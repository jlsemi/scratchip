
base_dir=.
base_dir_rel=../..
scratchip_dir=$(base_dir)/.scratchip
scratchip_dir_rel=$(base_dir_rel)/.scratchip

export MILL_LIB=$(scratchip_dir_rel)/jars
export COURSIER_CACHE=$(scratchip_dir_rel)/cache

verilog:
	chmod +x $(scratchip_dir)/mill
	cd $(base_dir)/hw/chisel; $(scratchip_dir_rel)/mill chisel.run -td $(base_dir_rel)/builds

export MILL_LIB={mill_lib_path}
export COURSIER_CACHE={mill_cache_path}

base_dir={prj_dir}
verilog:
	chmod +x {mill_path}
	{mill_path} chisel.run -td $(base_dir)/builds

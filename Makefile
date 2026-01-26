SIMULATOR_MAKE = make --no-print-directory -C ./simulator
CPU_MAKE = make --no-print-directory -C ./netlist_cpu

build:
	$(SIMULATOR_MAKE) build 
	$(CPU_MAKE) cpu

cpu_pipeline:
	$(CPU_MAKE) cpu_pipeline

run:
	$(CPU_MAKE) sim

clean:
	$(SIMULATOR_MAKE) clean
	$(CPU_MAKE) clean

.PHONY : clean
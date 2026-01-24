include config.mk

% : %.py
	mkdir -p build
	$(PYTHON_INTERPRETER) $(CAROTTE_PATH) -o ./build/$@.net ./$@.py
	cp ./build/$@.net ./build/current.net 

sim :
	$(SIMULATOR) ./build/current.net

all :
	make alu log_unit arith_unit demux mux regs forwarding hazards

update :
	make -C $(SIMULATOR_DIR) build

clean :
	rm -rf ./build/
	rm -rf ./__pycache__/

.PHONY: sim clean

from langchain.chains.base import Chain
from typing import Dict, List, Optional
from langchain.input import get_color_mapping

from langchain.callbacks.manager import (
    CallbackManagerForChainRun,
)

from typing import Dict, List

class ComponentIdenfierChain(Chain):
    chains: List[Chain]
    chained_input_key: str = 'input'
    output_key: str = 'output'
    
    @property
    def input_keys(self) -> List[str]:
        # Union of the input keys of the two chains.
        all_input_vars = set()
        for chain in self.chains:
            all_input_vars = all_input_vars.union(set(chain.input_keys))
        return list(all_input_vars)

    @property
    def output_keys(self) -> List[str]:
        return [self.output_key] + [f'chain_{i}' for i in range(len(self.chains))]

    def _call(self, 
              inputs: Dict[str, str],
              run_manager: Optional[CallbackManagerForChainRun] = None,
        ) -> Dict[str, str]:
        
        output = dict()
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
        color_mapping = get_color_mapping([str(i) for i in range(len(self.chains))])
        for i, chain in enumerate(self.chains):
            _output = chain.run(inputs, callbacks=_run_manager.get_child())
            output[f'chain_{i}'] = _output
            inputs[self.chained_input_key] = _output # set as input for next chain
            _run_manager.on_text(
                inputs, color=color_mapping[str(i)], end="\n", verbose=self.verbose
            )
            
        output[self.output_key] = _output
        return output
            
/* Copyright 2021 Karlsruhe Institute of Technology
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. */

import Rete from 'rete';

import {sockets, commonInputs, commonOutputs, BuiltinComponent} from 'core';
import PortControl from 'scripts/lib/workflows/controls/port-control';

const type = 'user-input';
const menu = 'User Input';

const inputs = [commonInputs.dep, {key: 'prompt', title: 'Prompt', socket: sockets.str}];
const commonOutputValues = {key: 'value', title: 'Value'};

const userInputText = new BuiltinComponent(
  'UserInputText',
  type,
  menu,
  inputs,
  [commonOutputs.dep, {...commonOutputValues, socket: sockets.str}],
);

const userInputInteger = new BuiltinComponent(
  'UserInputInteger',
  type,
  menu,
  inputs,
  [commonOutputs.dep, {...commonOutputValues, socket: sockets.int}],
);

const userInputFloat = new BuiltinComponent(
  'UserInputFloat',
  type,
  menu,
  inputs,
  [commonOutputs.dep, {...commonOutputValues, socket: sockets.float}],
);

const userInputBool = new BuiltinComponent(
  'UserInputBool',
  type,
  menu,
  inputs,
  [commonOutputs.dep, {...commonOutputValues, socket: sockets.bool}],
);

const userInputFile = new BuiltinComponent(
  'UserInputFile',
  type,
  menu,
  inputs,
  [commonOutputs.dep, {...commonOutputValues, socket: sockets.str}],
);

const userInputCropImages = new BuiltinComponent(
  'UserInputCropImages',
  type,
  menu,
  inputs.concat([{key: 'imagePath', title: 'Image Path', socket: sockets.str}]),
  [commonOutputs.dep, {key: 'cropInfo', title: 'Crop Info', socket: sockets.str}],
);

class ChooseComponent extends BuiltinComponent {
  constructor() {
    super(
      'UserInputChoose',
      type,
      menu,
      inputs,
      [commonOutputs.dep, {key: 'selected', title: 'Selected', socket: sockets.int}],
    );
  }

  builder(node) {
    super.builder(node);

    node.prevOptions = 0;
    node.addControl(new PortControl('options', 'Options'));

    this.editor.on('controlchanged', (control) => {
      if (control.parent !== node) {
        return;
      }

      const options = node.data.options;

      if (options > node.prevOptions) {
        for (let i = node.prevOptions; i < options; i++) {
          node.addInput(new Rete.Input(`option${i}`, `Option ${i + 1}`, sockets.str));
        }
      } else {
        for (let i = options; i < node.prevOptions; i++) {
          const input = node.inputs.get(`option${i}`);
          // Reverse loop since we are removing the connections as we loop.
          for (let j = input.connections.length - 1; j >= 0; j--) {
            this.editor.removeConnection(input.connections[j]);
          }
          node.removeInput(input);
        }
      }

      node.vueContext.$forceUpdate();
      node.prevOptions = options;
    });
  }

  fromFlow(flowNode) {
    const node = super.fromFlow(flowNode);

    node.data.options = flowNode.model.nOptions;
    for (let i = 0; i < node.data.options; i++) {
      node.inputs.set(`option${i}`, {connections: []});
    }

    return node;
  }

  toFlow(node) {
    const flowNode = super.toFlow(node);
    flowNode.model.nOptions = node.data.options;
    return flowNode;
  }
}

export default [
  userInputText,
  userInputInteger,
  userInputFloat,
  userInputBool,
  userInputFile,
  userInputCropImages,
  new ChooseComponent(),
];

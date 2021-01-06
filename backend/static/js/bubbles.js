

var nodes = new vis.DataSet([
  {label: "Comedy"},
  {label: "Romantic"},
  {label: "POLANI"},
  {label: "Action"},
  {label: "Horror"},
  {label: "Documentary"},
  {label: "Nature"},
  {label: "Drama"},
]);
var edges = new vis.DataSet();

var container = document.getElementById('bubbles');
var data = {
  nodes: nodes,
  edges: edges
};

nodeModuleColor = '#233A50';
nodeSelectedColor = '#AAAAAA';

var options = {
  nodes: {borderWidth:0,shape:"circle",color:{background:nodeModuleColor, highlight:{background:nodeModuleColor, border: 'white'}},font:{color:'#fff'}},
  interaction: {
    dragView: false,
    multiselect: true,
    zoomView: false
  },
  physics: {
    stabilization: false,
    minVelocity:  0.01,
    solver: "repulsion",
    repulsion: {
      nodeDistance: 50
    }
  }
};
var network = new vis.Network(container, data, options);


// Events
network.on("click", function(e) {
  if (e.nodes.length) {
    var node = nodes.get(e.nodes[0]);
    if (node.color === nodeSelectedColor) {
      if (typeof categories !== 'undefined') {
        const index = categories.indexOf(node.label);
        if (index > -1) { // label was found
          categories.splice(index, 1);
        }
      }
      node.color = {background: nodeModuleColor, highlight: {background: nodeModuleColor, border: nodeModuleColor}};
      node.labelHighlightBold = false;
    } else {
      if (typeof categories !== 'undefined') {
        const index = categories.indexOf(node.label);
        if (index === -1) { // label was not found
          categories.push(node.label);
        }
      }
      node.color = nodeSelectedColor;
      node.labelHighlightBold = false;
    }
    nodes.update(node);
  }
});

function draw_neo4j_graph(data) {
    // Переменные
    DJANGO_STATIC_URL = 'static';
    nodeItemMap = [];
    linkItemMap = [];
    let height = 600;
    let width = 1000;

    let neo4jDataItmArray = data.results[0].data;
    neo4jDataItmArray.forEach(function (dataItem) {
        //Создаем Nodes
        if (dataItem.graph.nodes != null && dataItem.graph.nodes.length > 0) {
            let neo4jNodeItmArray = dataItem.graph.nodes;
            neo4jNodeItmArray.forEach(function (nodeItm) {
                if (!(nodeItm.id in nodeItemMap))
                    nodeItemMap[nodeItm.id] = nodeItm;
            });
        }
        //Создаем Links
        if (dataItem.graph.relationships != null && dataItem.graph.relationships.length > 0) {
            let neo4jLinkItmArray = dataItem.graph.relationships;
            neo4jLinkItmArray.forEach(function (linkItm) {
                if (!(linkItm.id in linkItemMap)) {
                    linkItm.source = linkItm.startNode;
                    linkItm.target = linkItm.endNode;
                    linkItemMap[linkItm.id] = linkItm;
                }
            });
        }
    });
    console.log(nodeItemMap)
    console.log(linkItemMap)

    let svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height);

    let simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function (d) {
            return d.id;
        }).distance(50))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 3, height / 2));

    let link = svg.append("g")
        .selectAll("line")
        .data(linkItemMap)
        .enter().append("line")
        .attr("stroke", "black");

    let node = svg.append("g")
        .selectAll("circle")
        .data(nodeItemMap)
        .enter().append("circle")
        .attr("r", 20)
        // .style("fill", "url(" + "../" + DJANGO_STATIC_URL + "/js/man.ico" + ")")
        .call(d3.drag()
            .on("drag", dragged)
            .on("end", dragended));
    // .attr("fill", "crimson");

    let nodeImage = node.append("image")
        .attr("xlink:href", "../" + DJANGO_STATIC_URL + "/js/man.ico")
        .attr("height", "40")
        .attr("width", "40")
        .attr("x", -20)
        .attr("y", -20);

    simulation.nodes(nodeItemMap)
        .on("tick", ticked)
        .alphaDecay(0)
        .force("link")
        .links(linkItemMap);

    function ticked() {
        link
            .attr("x1", function (d) {
                return d.source.x;
            })
            .attr("y1", function (d) {
                return d.source.y;
            })
            .attr("x2", function (d) {
                return d.target.x;
            })
            .attr("y2", function (d) {
                return d.target.y;
            });
        node
            .attr("cx", function (d) {
                return d.x;
            })
            .attr("cy", function (d) {
                return d.y;
            });
    }

    function dragged(event, d) {
        d.x = event.x;
        d.y = event.y;
        // d3.select(this).raise().attr("transform", d=> "translate("+[d.x,d.y]+")" )
    }

    function dragended() {
        d3.select(this).attr("stroke", null);
    }
};
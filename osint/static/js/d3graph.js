function draw_neo4j_graph(data) {
    // Переменные
    DJANGO_STATIC_URL = 'static';
    nodeItemMap = [];
    linkItemMap = [];
    let height = 1000;
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

    let linksTypes = ['to_service, from_service']
    linksTypes = Array.from(new Set(linkItemMap.map(d => d.type)))
    let color = d3.scaleOrdinal(linksTypes, d3.schemeCategory10);
    console.log(nodeItemMap)
    console.log(linkItemMap)

    let svg = d3.select("#graph")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .call(d3.zoom()
            .on('zoom', (event) => {
                svg.attr('transform', event.transform);
            }));

    let tooltip = d3.select("body")
        .append("div")  // declare the tooltip div
        .attr("class", "tooltip")              // apply the 'tooltip' class
        .style("opacity", 0);                  // set the opacity to nil

    //  Формируем таблицу c инфой о вершине
    let nodeInfoTable = d3.select("#nodeInfo")
        .append("table")
        .attr('class', 'table table-striped')
        .attr('id', 'search_info');

     // Формируем таблицу c инфой о графе
    // let graphInfoTable = d3.select("#graphInfo")
    //     .append("table")
    //     .attr('class', 'table table-striped')
    //     .attr('id', 'graph_info')
    //     .append("tbody")
    //     .data(graphInfo)
    //     .enter()
    //     .append("tr")
    //     .append('td')
    //     .style('height', '50px')
    //     .style('font-size', '12pt')
    //     .attr('class', 'col-4')
    //     .attr('vertical-align', 'middle')
    //     .attr('text-align', 'center')
    //     .text(function (d) {
    //         return d.column;
    //     })
    //     .select(function() { return this.parentNode; })
    //     .append('td')
    //     .attr('class', 'dataNode')
    //     .text(function (d) {
    //         return d.value;
    //     })



    svg.selectAll("mydots")
        .data(linksTypes)
        .enter()
        .append("circle")
        .attr("cx", 100)
        .attr("cy", function (d, i) {
            return 100 + i * 25
        }) // 100 is where the first dot appears. 25 is the distance between dots
        .attr("r", 7)
        .style("fill", function (d) {
            return color(d)
        });

// Add one dot in the legend for each name.
    svg.selectAll("mylabels")
        .data(linksTypes)
        .enter()
        .append("text")
        .attr("x", 120)
        .attr("y", function (d, i) {
            return 100 + i * 25
        }) // 100 is where the first dot appears. 25 is the distance between dots
        .style("fill", function (d) {
            return color(d)
        })
        .text(function (d) {
            return d
        })
        .attr("text-anchor", "left")
        .style("alignment-baseline", "middle");
    // linksTypes.forEach(function (d){
    //
    //         .append('cirlce')
    //         .attr("r", 20)
    //         .style("fill", color(d))
    // });


    let simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function (d) {
            return d.id;
        }).distance(50))
        // .force("charge", d3.forceManyBody().strength(-200).distanceMax(400).distanceMin(60))
        .force("attractForce", d3.forceManyBody().strength(100).distanceMax(20).distanceMin(10))
        .force("collisionForce", d3.forceCollide(40).strength(0.3).iterations(10))
        // .force("charge", d3.forceCollide(12).strength(1).iterations(100))
        // .force("charge", d3.forceManyBody().strength(-140).distanceMax(50).distanceMin(10))
        .force("x", d3.forceX())
        .force("y", d3.forceY())
        .force("center", d3.forceCenter(width / 2, height / 2));


    svg.append("defs").selectAll("marker")
        .data(linksTypes)
        .join("marker")
        // .attr("id", d => `arrow-${d}`) для стрелок
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 22)
        .attr("refY", -1)
        .attr("markerWidth", 9)
        .attr("markerHeight", 9)
        .attr("orient", "auto")
        .append("path")
        .attr("fill", color)
        .attr("d", "M0,-5L10,0L0,5");

    // let links = svg.selectAll("foo") СТАРЫЕ ЛИНКИ
    //     .data(linkItemMap)
    //     .enter()
    //     .append("line")
    //     .style("stroke", "#ccc")
    //     .style("stroke-width", 1);

    const links = svg.append("g")
        .attr("fill", "none")
        .attr("stroke-width", 1.5)
        .selectAll("path")
        .data(linkItemMap)
        .join("path")
        .attr("stroke", d => color(d.type));
    // .attr("marker-end", d => `url(${new URL(`#arrow-${d.type}`, location)})`); для стрелок

    // let node = svg.selectAll("foo") СТАРЫЕ НОДЫ
    //     .data(nodeItemMap)
    //     .enter()
    //     .append("g")
    //     .call(d3.drag()
    //         .on("start", dragstarted)
    //         .on("drag", dragged)
    //         .on("end", dragended));

    const node = svg.append("g")
        .attr("fill", "currentColor")
        .attr("stroke-linecap", "round")
        .attr("stroke-linejoin", "round")
        .selectAll("g")
        .data(nodeItemMap)
        .join("g")
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));


    let nodeCircle = node.append("circle")
        .attr("r", 15)
        .attr("stroke", "gray")
        .attr("stroke-width", "2px")
        .attr("fill", "white");

    let nodeImage = node.append("image")
        // Инфа о вершине
        .on("click", function(event, data) {
            nodeInfoTable.selectAll("tbody").remove()
            let inputData = []
            inputData.push({column: 'Тип данных', value: data.labels.indexOf('Data') !== -1 ? data.properties['data_type'] : data.properties['service_name']});
            inputData.push({column: 'Данные', value: data.labels.indexOf('Data') !== -1 ? data.properties['data'] : 'Сервис'});
            let date = unixTime(data.labels.indexOf('Data') !== -1 ? findReceiptTime(data.id) : '');
            inputData.push({column: 'Время получения', value: date});

            let nodeInfo = nodeInfoTable.append("tbody");
                nodeInfo.selectAll("tr")
                    .data(inputData)
                    .enter()
                    .append("tr")
                    .append('td')
                    .style('height', '50px')
                    .style('font-size', '12pt')
                    .attr('class', 'col-4')
                    .attr('vertical-align', 'middle')
                    .attr('text-align', 'center')
                    .text(function (d) {
                        return d.column;
                    })
                    .select(function() { return this.parentNode; })
                    .append('td')
                    .attr('class', 'dataNode')
                    .text(function (d) {
                        return d.value;
                    })
        })
        .on("mouseover", function (event, data) {
            // Показать инфу о вершине
            tooltip.transition()
                .duration(200)
                .style("opacity", .9);
            tooltip.html(
                "</a>" +
                "<br/>" + (data.labels.indexOf('Data') !== -1 ? data.properties['data'] : data.properties['service_name']))
                .style("left", (event.pageX) + "px")
                .style("top", (event.pageY - 45) + "px");
        })
        .on('mouseout', function (d) {
            // Спрятать инфу о вершине
            d3.selectAll(".tooltip")
                .transition()
                .duration(100)
                .style("opacity", 0);
        })
        .attr("xlink:href", function (d) {
            if (d.labels.indexOf('Data') !== -1)
                if (d.properties['data_type'].includes('vk-'))
                    return "../" + DJANGO_STATIC_URL + "/js/vk.ico";
                else if (d.properties['data_type'].includes('phones-'))
                    return "../" + DJANGO_STATIC_URL + "/js/phone.ico";
                else if (d.properties['data_type'].includes('emails-'))
                    return "../" + DJANGO_STATIC_URL + "/js/email.ico";
                else
                    return "../" + DJANGO_STATIC_URL + "/js/man.ico";
            else if (d.labels.indexOf('Service') !== -1)
                return "../" + DJANGO_STATIC_URL + "/js/service.ico";
        })
        // .attr("xlink:href", )
        .attr("height", "40")
        .attr("width", "40")
        .attr("x", -20)
        .attr("y", -20);

    let texts = node.append("text")
        .attr("dx", 20)
        .attr("dy", 8)
        .text(function (d) {
            if (d.labels.indexOf('Data') !== -1)
                return d.properties['data_type'];
            else if (d.labels.indexOf('Service') !== -1)
                return d.properties['service_name']
            return d.id;
        })
        .clone(true).lower()
        .attr("fill", "none")
        .attr("stroke", "white")
        .attr("stroke-width", 3);

    simulation.nodes(nodeItemMap)
        .on("tick", ticked)
        .force("link")
        .links(linkItemMap);

    function ticked() {
        links.attr("d", linkArc);
        node.attr("transform", d => `translate(${d.x},${d.y})`);
    }

    function linkArc(d) {
        const r = Math.hypot(d.target.x - d.source.x, d.target.y - d.source.y);
        return `
    M${d.source.x},${d.source.y}
    A${r},${r} 0 0,1 ${d.target.x},${d.target.y}
  `;
    }

    function dragstarted(d) {
        // if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        simulation.restart();
        simulation.alpha(0.3);
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(event, d) {
        d.x = event.x;
        d.y = event.y;
        // d3.select(this).raise().attr("transform", d=> "translate("+[d.x,d.y]+")" )
    }

    function dragended() {
        simulation.alphaTarget(0);
        d3.select(this).attr("stroke", null);
    }

    function unixTime(unixtime) {
        if (unixtime === "")
            return "";
        let u = new Date(unixtime*1000);

          return u.getUTCHours() +
            ':' + ('0' + u.getUTCMinutes()).slice(-2) +
            ':' + ('0' + u.getUTCSeconds()).slice(-2) +
            ' ' + (' ' + u.getUTCDate()).slice(-2) +
            '.' + ('0' + u.getUTCMonth()).slice(-2) +
            '.' + ('' + u.getUTCFullYear()).slice()
    };

    function findReceiptTime(nodeId) {
        let receipt_timestamp = ""
        linkItemMap.forEach(function (linkItm){
            if (linkItm.endNode == nodeId){
                receipt_timestamp =linkItm.properties['receipt_timestamp'];
            }
        })
        return receipt_timestamp;
    }
};

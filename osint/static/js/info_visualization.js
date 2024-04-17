let viz;
function visualization(info) {
    let timestamp = info.service_info.search_timestamp;
    $('#search_info').find('tbody')
        .append($.map(info.output_data, function (info, infoType) {
                return $('<tr>', {
                    'class': 'deleteTr'
                })
                    .append($('<td>', {
                        'text': infoType
                    }))
                    .append($('<td>', {
                        'text': timestamp,
                        'style': 'text-align: center;'
                    }))
                    .append($('<td>', {
                        'text': info,
                        'style': 'text-align: center;'
                    }))
                    .append($('<td>')
                        .append($('<input>', {
                            'value': 'del',
                            'type': 'button',
                            'class': 'deleteButton',
                            'style': 'text-align: center;',
                            'onclick': 'deleteStr(this.parentNode.parentNode)'
                        }))
                    )
            })
        );
}



// function drawGraph() {
//     let config = {
//                 container_id: "viz",
//                 server_url: "bolt://neo4j:7687",
//                 server_user: "neo4j",
//                 server_password: "neo4j",
//                 labels: {
//                     "Service": {
//                         "caption": "service_name",
//                         "size": "2",
//                         "community": "community",
//                         "title_properties": [
//                             "service_name",
//                         ]
//                     },
//                     "Data": {
//                         "caption": "data_type",
//                         "size": "2",
//                         "community": "community",
//                         "title_properties": [
//                             "data_type",
//                             "data",
//                         ]
//                     },
//                 },
//                 relationships: {
//                     "to_service": {
//                         "caption": true,
//                     },
//                     "from_service": {
//                         "caption": true,
//                     }
//                 },
//                 arrows: true,
//                 initial_cypher: "MATCH (n) RETURN n"
//             };
//
//             viz = new NeoVis.default(config);
//             viz.render();
//             console.log(viz);
//             console.log('viz');
// }
// $("#reload").click(function() {
//
// 		let cypher = $("#cypher").val();
//
// 		if (cypher.length > 3) {
// 			viz.renderWithCypher(cypher);
// 		} else {
// 			console.log("reload");
// 			viz.reload();
//
// 		}
//
// 	});
//
// 	$("#stabilize").click(function() {
// 		viz.stabilize();
// 	})

// https://d3-graph-gallery.com/arc.html

class ChordDiagram {
    
    constructor(defaultConfig, _data) {
        this.config = {
            parentElement: defaultConfig.parentElement,
            containerWidth: defaultConfig.containerWidth || 600,
            containerHeight: defaultConfig.containerHeight || 600,
            margin: {top: 5, right: 5, bottom: 20, left: 20},
            tooltipPadding: defaultConfig.tooltipPadding || 15,
        }
        this.data = _data
        this.mainCharacters = mainCharacters.slice(0,10)

        this.initVis()
	}
	
	initVis() {
		let vis = this

        vis.colors = ['#F25041', '#F25041', '#38B000', '#F25041', '#F25041', '#8C1F66', '#33A6A6', '#323673', '#F25041', '#323673' ]

		vis.width = vis.config.containerWidth - vis.config.margin.left - vis.config.margin.right
	  	vis.height = vis.config.containerHeight - vis.config.margin.top - vis.config.margin.bottom
		
		vis.svg = d3.select(vis.config.parentElement)
	  		.attr('width', vis.config.containerWidth)
	  		.attr('height', vis.config.containerHeight)
			
		let matrix = vis.getMatrix()

        vis.chordArc = d3.chord()
            .padAngle(0.05)
            .sortSubgroups(d3.descending)
            (matrix)

        vis.svg //chord labels
            .datum(vis.chordArc)
            .append('g')
            .attr("transform", `translate(${vis.config.containerWidth/2},${ vis.config.containerHeight/2})`)
            .selectAll('g')
            .data(d => d.groups)
            .join('text')
                .each(d => {d.angle = (d.startAngle + d.endAngle)/2} )
                .attr('class', 'chord-titles')
                .attr('x', '5')
                .attr('dy', '.35em')
                .attr('text-anchor', d => { (d.angle > Math.PI) ? 'end' : null}) // if the chord angle isnt possible, get it out of here
                .attr('font-size', '11')
                .attr('font-family', 'sans-serif')
                .attr('transform', d => {return "rotate(" +(d.angle*180/Math.PI - 90) + ")" + "translate(" + (272) + ")" + (d.angle>Math.PI? "rotate(180)" : "")})
                .style('fill', 'black')
                .text(d => vis.mainCharacters[d.index])

        vis.svg // group links
            .datum(vis.chordArc)
            .append('g')
            .attr("transform", `translate(${vis.config.containerWidth/2},${ vis.config.containerHeight/2})`)
            .selectAll('g')
            .data(d => d.groups)
            .join('path')
                .attr('class', d => {return 'speaker ' + vis.mainCharacters[d.index] })
                .attr('id', d => { return '#speaker ' + vis.mainCharacters[d.index] })
                .style('stroke', 'black')
                .style('fill', d => vis.colors[d.index]) // fix later
                .style('opacity', '0.7')
                .attr('d', d3.arc().innerRadius(200).outerRadius(210))
            
        vis.svg // chord links between groups
            .datum(vis.chordArc)
            .append("g")
			.attr("transform", `translate(${vis.config.containerWidth/2},${ vis.config.containerHeight/2})`)
            .selectAll('path') // chord links between groups
            .data(d => d)
            .join('path')
                .attr('d', d3.ribbon().radius(200))
                .style('fill', d => vis.colors[d.source.index%19]) //update later
                .style('opacity', '0.5')
                .style('stroke', 'black')
            .on('mouseover', (event, d) => {
                d3.select('#tooltip')
                    .style('display', 'block')
                    .style('left', (event.pageX + vis.config.tooltipPadding) + 'px')
                    .style('top', (event.pageY + vis.config.tooltipPadding) + 'px')
                    .html(`
                        <div class="tooltip-title">${vis.mainCharacters[d.source.index]}:</div>
                        <ul>
                        <li>Mentioned ${vis.mainCharacters[d.target.index]} ${d.source.value} times</li>
                        <li>Mentioned by ${vis.mainCharacters[d.target.index]} ${d.target.value} times</li>
                        </ul>`)
                })
            .on('mouseleave', () => {
                d3.select('#tooltip').style('display', 'none')
            })




    }

    getMatrix() {
        let vis = this

        let matrix = Array(vis.mainCharacters.length).fill(null).map(() => Array(vis.mainCharacters.length).fill(0)) // space savers

        let mainCharactersRE = new RegExp(vis.mainCharacters.join('|'), 'gm') // find every single mention match

        vis.data.forEach(d => {
            //console.log('data: ', d.dialogue)
            let characterMention = new Set(d.dialogue.match(mainCharactersRE))
            if (characterMention.size != 0 && d.character.match(mainCharactersRE)) {
                characterMention.forEach(cm => {
                    let speakerIndex = vis.mainCharacters.indexOf(d.character)
                    let referenceIndex = vis.mainCharacters.indexOf(cm)

                    matrix[speakerIndex][referenceIndex] += 1 // yeah array of arrays
                })
            }
        })
        return matrix

    }
}
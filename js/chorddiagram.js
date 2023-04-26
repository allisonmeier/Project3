// https://d3-graph-gallery.com/arc.html

class ChordDiagram {
    
    constructor(defaultConfig, _data) {
        this.config = {
            parentElement: defaultConfig.parentElement,
            containerWidth: defaultConfig.containerWidth || 600,
            containerHeight: defaultConfig.containerHeight || 600,
            margin: {top: 5, right: 5, bottom: 20, left: 20},
        }
        this.data = _data
        this.mainCharacters = mainCharacters

        this.initVis()
	}
	
	initVis() {
		let vis = this

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

        vis.svg
            .datum(vis.chordArc)
            .append('g')
            .attr("transform", `translate(${vis.config.containerWidth/2},${ vis.config.containerHeight/2})`)
            .selectAll('g')
            .data(d => d.groups)
            .join('text') // chord labels
                .each(d => {d.angle = (d.startAngle + d.endAngle)/2} )
                .attr('class', 'chord-titles')
                .attr('x', '5')
                .attr('dy', '.35em')
                .attr('text-anchor', d => { d.angle > Math.PI ? 'end' : null}) // if the chord angle isnt possible, get it out of here
                .attr('transform', d => { `rotate(${(d.angle * 180)/Math.PI - 90})translate(${270})${d.angle > Math.PI? "rotate(180)" : ""}` })
                .style('fill', 'black')
                .text(d => vis.mainCharacters[d.index])
            .join('path') // group links
                .attr('class', d => {return 'speaker ' + vis.mainCharacters[d.index] })
                .attr('id', d => { return '#speaker ' + vis.mainCharacters[d.index] })
                .style('stroke', 'black')
                .style('opacity', '0.6')
                .attr('d', d3.arc()
                    .innerRadius(200)
                    .outerRadius(210))
            .join('path') // chord links between groups


    }


    updateVis() {let vis = this}


    renderVis() {let vis = this}

    /* 
    matrix format:
    
    
    
    */



    getMatrix() {
        let vis = this

        let matrix = Array(vis.mainCharacters.length)
            .fill(null) //space saver for characters
            .map(() => Array(vis.mainCharacters.length).fill(0)) // space saver for nums

        let mainCharactersRE = new RegExp(vis.mainCharacters.join(' '), 'gm') // find every single mention match

        vis.data.forEach(d => {
            let characterMention = new Set(d.dialogue.match(mainCharactersRE))

            if (characterMention.size != 0) {
                characterMention.forEach(cm => {
                    let speaker = vis.mainCharacters.indexOf(d.character)
                    let reference = vis.mainCharacters.indexOf(cm)

                    matrix[speaker][reference] += 1 // yeah array of arrays
                })
            }
        })
        return matrix

    }





}
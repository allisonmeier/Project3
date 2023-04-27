// https://observablehq.com/@d3/sankey
// https://d3-graph-gallery.com/graph/sankey_basic.html

//import * as d3 from "d3"
//import * as d3Sankey from "d3-sankey"

//var sankey = d3.sankey();

class SankeyDiagram {
    
    constructor(defaultConfig, _data) {
        this.config = {
            parentElement: defaultConfig.parentElement,
            containerWidth: defaultConfig.containerWidth || 600,
            containerHeight: defaultConfig.containerHeight || 600,
            margin: {top: 5, right: 5, bottom: 20, left: 20},
            tooltipPadding: defaultConfig.tooltipPadding || 15,
        }
        this.data = _data
        this.mainCharacters = mainCharacters
        this.seasonsList = ['01', '02', '03', '04', '05']

        this.initVis()
	}

    initVis() {
        let vis = this
        let nodeAlign = 'justify'

        vis.colors = [ 'orange' ]

        vis.matrix = vis.getMatrix()

		vis.width = vis.config.containerWidth - vis.config.margin.left - vis.config.margin.right
	  	vis.height = vis.config.containerHeight - vis.config.margin.top - vis.config.margin.bottom
		
		vis.svg = d3.select(vis.config.parentElement)
	  		.attr('width', vis.config.containerWidth)
	  		.attr('height', vis.config.containerHeight)





    }

    updateVis() {let vis = this}


    renderVis() {let vis = this}

    /*
    matrix format:

    Uhtred, [11, 3, 4, etc] (number of appearances in episodes 1-46)
    Stiorra, [0, 0, 1, etc]
    etc [etc]
    etc
    
    */

    // works: haven't worked past this yet
    getMatrix() {
        let vis = this

        let matrix = Array(vis.mainCharacters.length).fill(null).map(() => Array(vis.seasonsList.length).fill(0)) // space savers
        //console.log(matrix)

        let seasonsRE = new RegExp(vis.seasonsList.join('|'), 'gm') // find every single mention match
        //console.log(seasonsRE)

        vis.data.forEach(d => {

            let characterAppearance = new Set(d.season.match(seasonsRE))
            console.log(characterAppearance)

            if (characterAppearance.size >= 0 && d.season.match(seasonsRE)) {
                characterAppearance.forEach(ca => {
                    let characterIndex = vis.seasonsList.indexOf(d.character)
                    let seasonIndex = vis.seasonsList.indexOf(ca)

                    matrix[characterIndex][seasonIndex] += 1 // yeah array of arrays
                })
            }
        })
        console.log(matrix)
        return matrix

    }



}
class WordMap {

    /* this should show words spoken most overall, 
    and eventually per character*/

    constructor(defaultConfig, _data) {
        this.config = {
            parentElement: defaultConfig.parentElement,
            containerWidth: defaultConfig.containerWidth || 700,
            containerHeight: defaultConfig.containerHeight || 300,
            margin: defaultConfig.margin || {top: 5, right: 5, bottom: 20, left: 20},
        }
        this.data = _data
        this.initVis()
    }

    initVis(){
        let vis = this
        let words 

        let wordFrequency = []

        vis.data.forEach(d => {
            words = d.dialog
                .replace(/[^a-z\s]/igm,'') // replaces anything other than letters or spaces, with ''
                .toLowerCase() // makes every single letter lowercase
                .split(/\s/gm) // splits everything in the string even the long ones
                .filter(string => string) //filters out dud empties
            words.forEach(word => {
                if (!vis.wordFrequency[word]) {
                    vis.wordFrequency[word] = 1
                } else {
                    vis.wordFrequency[word] += 1
                }
                
            })
        
            })

        console.log(words)

        vis.width = vis.config.containerWidth + vis.config.margin.left + vis.config.margin.right;
        vis.height = vis.config.containerHeight + vis.config.margin.top + vis.config.margin.bottom;
    
        vis.sizeScale = d3.scaleLinear()
            .range([20, 40])     
    
        vis.svg = d3.select(vis.config.parentElement)
            .append('svg')
                .attr('width', vis.width + vis.config.margin.left + vis.config.margin.right)
                .attr('height', vis.height + vis.config.margin.top + vis.config.margin.bottom)
                .append('g')
                .attr('transform', `translate(${vis.config.margin.left},${vis.config.margin.top})`)

        vis.updateVis()
    }

    updateVis() {
        


        
    }

    renderVis() {

    }


}
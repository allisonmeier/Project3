class Barchart {

    /* this should show words spoken per character, 
    and maybe eventually episodes appeared in per character*/

    constructor(defaultConfig, _data) {
        this.config = {
            parentElement: defaultConfig.parentElement,
            containerWidth: defaultConfig.containerWidth || 700,
            containerHeight: defaultConfig.containerHeight || 300,
            margin: defaultConfig.margin || {top: 5, right: 5, bottom: 20, left: 30},
            tooltipPadding: defaultConfig.tooltipPadding || 15,
        }
        this.data = _data.filter(d => d.character != 'man')
        this.initVis()
    }

    initVis() {
        let vis = this

        vis.width = vis.config.containerWidth - vis.config.margin.left - vis.config.margin.right
        vis.height = vis.config.containerHeight - vis.config.margin.top - vis.config.margin.bottom
    
        // Initialize scales
        vis.xScale = d3.scaleBand()
            .range([0, vis.width])
            .padding(0.1)
    
        vis.yScale = d3.scaleLinear()
            .range([0, vis.height])

        vis.colorScale = [ '#F25041', '#F25041', '#38B000', '#F25041', '#F25041', '#8C1F66', '#F25041', '#323673', '#F25041', '#323673', '#F25041', '#F25041', '#F25041', '#F25041', '#F25041', '#33A6A6', '#F25041', '#323673', '#F25041']

        vis.xAxis = d3.axisBottom(vis.xScale)
            .ticks(10)
    
        vis.yAxis = d3.axisLeft(vis.yScale)
            .ticks(10)        
    
        vis.svg = d3.select(vis.config.parentElement)
            .attr('width', vis.config.containerWidth)
            .attr('height', vis.config.containerHeight);

        vis.chart = vis.svg.append('g')
            .attr('transform', `translate(${vis.config.margin.left},${vis.config.margin.top})`)

        vis.xAxisG = vis.chart.append('g')
            .attr('class', 'axis x-axis')
            .attr('transform', `translate(0, ${vis.height})`)

        vis.yAxisG = vis.chart.append('g')
            .attr('class', 'axis y-axis')

        // vis.append all the text stuff like axes titles 

        
    }


    updateVis() {
        let vis = this
        let characterWordsMap, charactersInEpisodesMap

        // character and the sum of all the words spoken in ALL their dialogues
        characterWordsMap = d3.rollups(vis.data, w => d3.sum(w, d => d.dialogue.split(' ').length), d => d.character)
        
        vis.characterWords = Array
            .from(characterWordsMap, ([character, numOfWords]) => ({character, numOfWords}))
            .sort((a,b) => b.numOfWords - a.numOfWords)

        console.log(vis.characterWords)

        // only show characters who actually speak in that episode/season/whenever
        vis.charactersWhoSpeak = []
        

        //group by chracter then filter
        let charactersDialogueMap = d3.group(vis.data, d => d.character) // group by season, subgroup by episode, subgroup by characters in episode
        
        // right now this includes everyone, so i prob need to remove characters with < 5 lines i think

        // count through csv by character 

        vis.charactersDialogue = Array // note to self: remove "man"
            .from(charactersDialogueMap, function(entry) {
                return {character: entry[0], dialogue: entry[1]}
            })
            .sort((a,b) => b.dialogue.length - a.dialogue.length)

        //console.log(vis.charactersDialogue)


        console.log(vis.charactersWhoSpeak)
        console.log(vis.characterInEpisodes)

        vis.charactersDialogue = vis.charactersDialogue.slice(0,19)

        vis.xValue = d => d.character
        vis.yValue = d => d.dialogue.length
        
        vis.xScale.domain(vis.charactersDialogue.map(vis.xValue))
        vis.yScale.domain([d3.max(vis.charactersDialogue, vis.yValue), 0])

        vis.renderVis()
    }

    renderVis() {
        let vis = this

        vis.bars = vis.chart.selectAll('.bar')
            .data(vis.charactersDialogue)
            .enter()
            .append('rect')
                .attr('class', 'bar')
                .attr('width', vis.xScale.bandwidth())
                .attr('y', d => vis.yScale(vis.yValue(d)))
                .attr('x', d => vis.xScale(vis.xValue(d)))
                .attr('height', d => vis.height - vis.yScale(vis.yValue(d)))
                .attr('fill', vis.colorScale)  // to-do
            .on('mouseover', (event, d) => {
                d3.select('#tooltip')
                    .style('display', 'block')
                    .style('left', (event.pageX + vis.config.tooltipPadding) + 'px')
                    .style('top', (event.pageY + vis.config.tooltipPadding) + 'px')
                    .html(`
                        <div class="tooltip-title">${d.character}:</div>
                        <ul>
                        <li>Spoke ${d.dialogue.length} times</li>
                        </ul>`)
                })
            .on('mouseleave', () => {
                d3.select('#tooltip').style('display', 'none')
            })
    
            vis.xAxisG.call(vis.xAxis)
            vis.yAxisG.call(vis.yAxis)
            
    }

}

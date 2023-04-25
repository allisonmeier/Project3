class Barchart {

    /* this should show words spoken per character, 
    and maybe eventually episodes appeared in per character*/


    constructor(defaultConfig, _data) {
      // Configuration object with defaults
      // Important: depending on your vis and the type of interactivity you need
      // you might want to use getter and setter methods for individual attributes
      this.config = {
        parentElement: defaultConfig.parentElement,
        containerWidth: defaultConfig.containerWidth || 700,
        containerHeight: defaultConfig.containerHeight || 300,
        margin: defaultConfig.margin || {top: 5, right: 5, bottom: 20, left: 20},
      }
      this.data = _data
      this.initVis();
    }

    initVis() {
        let vis = this

        vis.width = vis.config.containerWidth - vis.config.margin.left - vis.config.margin.right
        vis.height = vis.config.containerHeight - vis.config.margin.top - vis.config.margin.bottom
    
        // Initialize scales
        vis.xScale = d3.scaleLinear()
            .range([0, vis.width])
            .paddingInner(0.1)
    
        vis.yScale = d3.scaleBand()
            .range([0, vis.height])

        // TO-DO: vis.colorScale

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
            .attr('transform', `translate(${vis.config.margin.left})`)

        vis.yAxisG = vis.chart.append('g')
            .attr('class', 'axis y-axis')

        // vis.append all the text stuff like axes titles 

    }


    updateVis() {
        let vis = this

        // character and the sum of all the words spoken in ALL their dialogues
        characterWordsMap = d3.rollups(vis.data, d3.sum(w, d => d.dialogue.split(' ').length), d => d.character)
        
        vis.characterWords = Array
            .from(characterWordsMap, ([character, numOfWords]) => ({character, numOfWords}))
            .sort((a,b) => b.count - a.count)

        // only show characters who actually speak in that episode/season/whenever
        vis.charactersWhoSpeak = []
        
        charactersInEpisodesMap = d3.group(vis.data, d => d.season, d => d.episode, d => d.character) // group by season, subgroup by episode, subgroup by characters in episode
        vis.characterInEpisodes = Array.from(charactersInEpisodesMap, ([season, episodes]) => ({season, episodes}))
        vis.characterInEpisodes.forEach(i => {
                i.episodes = Array.from(i.episodes, ([episode, characters]) => ({episode, characters}))
                i.episodes.forEach(episode => {
                        episode.characters = Array.from(episode.characters, ([character, dialogue]) => ({character, dialogue}))
                        episode.characters.forEach(character => {
                            if (!vis.charactersWhoSpeak[character]) {
                                vis.charactersWhoSpeak =1
                            } else {
                                vis.charactersWhoSpeak[character] += 1
                            }
                        })
                    })
                })

        // right now this includes everyone, so i prob need to remove characters with < 5 lines i think
        
        vis.yScale.domain(vis.charactersWhoSpeak.map(vis.xValue))
        vis.xScale.domain([0, d3.max(vis.charactersWhoSpeak, vis.yValue)])

        vis.renderVis()
    }

    renderVis() {
        let vis = this



    }

}

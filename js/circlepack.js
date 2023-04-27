// https://www.d3indepth.com/hierarchies/
// https://vizhub.com/tasqon/79f220b21a5345418740a402bac98cee
// https://observablehq.com/@d3/pack


// if this is too difficult to learn upfront, dendogram or tree map are two alternatives


// data info to add manually: https://listofdeaths.fandom.com/wiki/The_Last_Kingdom#Deaths

class CirclePack {
    constructor(defaultConfig) {
        this.config = {
            parentElement: defaultConfig.parentElement,
            containerWidth: defaultConfig.containerWidth || 600,
            containerHeight: defaultConfig.containerHeight || 600,
            margin: {top: 5, right: 5, bottom: 20, left: 20},
            tooltipPadding: defaultConfig.tooltipPadding || 15,
        }

        // character death data!
        d3.csv('../character-deaths.csv')
            .then(_data => {
                data = _data
                data.forEach(d => {
                d.character = d.character,
                d.death = d.death,
                d.killer = d.killer
                })
            })

        this.data = data
        this.mainCharacters = mainCharacters.slice(0,10)

        this.initVis()
	}

    initVis() {
        let vis = this

        /* Categories:

        Other
        - Survived
        - Unknown

        Weapon
        - Projectile: Arrow, Spear
        - Handheld: Knife, Sword, Axe, Decapitation
        
        Non-Weapon
        - Falling Harm: Fall, Impaled (Candlestick)
        - Miscellaneous Harm: Hounds, Fire, Strangled, Drowned
        - Natural: Illness, Age, Childbirth
        - Injury: Injury (Broken Neck), Injury (Head)

        */

        const hierarchy =  {
            name: 'All Character Deaths',
            children: [
                {
                    name: 'No Death',
                    children: [
                        {name: 'Survived', value: 23},
                        {name: 'Unknown', value: 2}
                    ]
                },
                {
                    name: 'Weapon',
                    children: [
                        {
                            name: 'Projectile Weapon',
                            children: [
                                {name: 'Arrow', value: 3},
                                {name: 'Spear', value: 2}
                            ]
                        },
                        {
                            name: 'Handheld Weapon',
                            children: [
                                {name: 'Knife', value: 7},
                                {name: 'Sword', value: 10},
                                {name: 'Axe', value: 2}
                            ]
                        }
                    ]
                },
                {
                    name: 'Non-Weapon',
                    children: [
                        {
                            name: 'Falls',
                            children: [
                                {name: 'Fall', value: 1},
                                {name: 'Impaled (Candlestick)', value: 1}
                            ]
                        },
                        {
                            name: 'Miscellaneous',
                            children: [
                                {name: 'Hounds', value: 1},
                                {name: 'Fire', value: 2},
                                {name: 'Strangled', value: 1},
                                {name: 'Drowned', value: 2}
                            ]
                        },
                        {
                            name: 'Natural Causes',
                            children: [
                                {name: 'Illness', value: 2},
                                {name: 'Age', value: 1},
                                {name: 'Childbirth', value: 1}
                            ]
                        },
                        {
                            name: 'Injury',
                            children:[
                                {name: 'Injury (Broken Neck)', value: 1},
                                {name: 'Injury (Head)', value: 1}
                            ]
                        }
                    ]
                }
            ]
        }

        //console.log(hierarchy)

    }

    updateVis() {
        let vis = this

    }

    renderVis() {
        let vis = this

    }

}





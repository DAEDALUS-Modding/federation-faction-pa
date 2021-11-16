var newBuild = {
"/pa/units/paeiou/light_infantry/conscript/conscript.json": ["fed_light_inf", 0,{ row: 0, column: 1, titans: true }],
"/pa/units/paeiou/light_infantry/fac_light_infantry/fac_light_infantry.json": ["fed_factory", 0,{ row: 0, column: 0, titans: true }],
"/pa/units/paeiou/light_infantry/gust/gust.json": ["fed_light_inf", 0,{ row: 0, column: 2, titans: true }],
"/pa/units/paeiou/light_infantry/light_inf_fab/light_inf_fab.json": ["fed_light_inf", 0,{ row: 0, column: 2, titans: true }],

}
if (Build && Build.HotkeyModel && Build.HotkeyModel.SpecIdToGridMap) {
_.extend(Build.HotkeyModel.SpecIdToGridMap, newBuild);
}
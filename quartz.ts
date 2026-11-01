import { loadQuartzConfig, loadQuartzLayout } from "./quartz/plugins/loader/config-loader"

import * as ExternalPlugin from "./.quartz/plugins"

// Список в папке: сортировка по названию файла (ГГ.ММ.ДД), старые сверху
ExternalPlugin.FolderPage({
    sort: (a, b) => {
        const x = a.slug ?? ""
        const y = b.slug ?? ""
        return x < y ? -1 : x > y ? 1 : 0
    },
})

const config = await loadQuartzConfig()
export default config
export const layout = await loadQuartzLayout()

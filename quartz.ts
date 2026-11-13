import { loadQuartzConfig, loadQuartzLayout } from "./quartz/plugins/loader/config-loader"
import { FolderPage } from "@quartz-community/folder-page"
import type { SortFn } from "@quartz-community/types"
import { byDateAndAlphabetical, isFolderPath } from "@quartz-community/utils"

const config = await loadQuartzConfig()

// Lecture filenames start with their class date; keep their cards in that order
// while leaving the standard folder ordering intact everywhere else.
const defaultDateSort = byDateAndAlphabetical()
const defaultFolderSort: SortFn = (first, second) => {
  const firstIsFolder = isFolderPath(first.slug ?? "")
  const secondIsFolder = isFolderPath(second.slug ?? "")
  if (firstIsFolder && !secondIsFolder) return -1
  if (!firstIsFolder && secondIsFolder) return 1
  return defaultDateSort(first, second)
}
const lectureDate = (slug: string | undefined, title: string | undefined): string | undefined =>
  slug?.startsWith("лекции/") ? title?.match(/^(\d{2}\.\d{2}\.\d{2})(?:\s|$)/)?.[1] : undefined

const sortFolderPages: SortFn = (first, second) => {
  const firstDate = lectureDate(first.slug, first.frontmatter?.title)
  const secondDate = lectureDate(second.slug, second.frontmatter?.title)
  return firstDate && secondDate
    ? secondDate.localeCompare(firstDate)
    : defaultFolderSort(first, second)
}

const folderPageIndex = config.plugins.pageTypes?.findIndex(
  (pageType) => pageType.name === "FolderPage",
)
if (folderPageIndex !== undefined && folderPageIndex !== -1 && config.plugins.pageTypes) {
  config.plugins.pageTypes[folderPageIndex] = FolderPage({
    showFolderCount: false,
    sort: sortFolderPages,
  })
}

export default config
export const layout = await loadQuartzLayout()

export const endpoints = {
  shortcodes: {
    latest: 'cms_shortcodes/pages/latest/',
    templates: 'cms_shortcodes/templates/',
    pages: 'cms_shortcodes/pages/',
    instances: 'cms_shortcodes/instances/',
    instancesTree: 'cms_shortcodes/instances/tree/',
    categories: 'cms_shortcodes/categories/',
    pageByPath: 'cms_shortcodes/pages/by_path/',
    layout: 'cms_shortcodes/layout/',
  },
  categories: {
    list: 'settings/categories/',
    create: 'settings/categories/',
    update: (id) => `settings/categories/${id}/`,
    delete: (id) => `settings/categories/${id}/`
  },
  tags: {
    list: 'settings/tags/',
    create: 'settings/tags/',
    update: (id) => `settings/tags/${id}/`,
    delete: (id) => `settings/tags/${id}/`
  }
}

export default {
  Shortcodes: {
    path: '/shortcodes',
    component: '@/modules/cms_shortcodes/client/src/ParentLayout.vue',
    redirect: 'MainShortcodePage',
    meta: {
      title: 'Конструктор сайта',
      requiresAuth: true
    }
  },
  MainShortcodePage: {
    path: '/shortcodes/editor',
    component: '@/modules/cms_shortcodes/client/src/editor/MainPage.vue',
    meta: {
      title: 'Главная',
      requiresAuth: true
    }
  },
  ShortcodeEditor: {
    path: '/shortcodes/editor/:id?',
    component: '@/modules/cms_shortcodes/client/src/editor/ShortcodeEditor.vue',
    meta: {
      title: 'Редактор страниц',
      requiresAuth: true
    }
  },
  Templates: {
    path: '/shortcodes/templates',
    component: '@/modules/cms_shortcodes/client/src/editor/TemplateManager.vue',
    meta: {
      title: 'Компоненты',
      requiresAuth: true
    }
  },
  Layouts: {
    path: '/shortcodes/site-layouts',
    component: '@/modules/cms_shortcodes/client/src/SiteLayout.vue',
    meta: {
      title: 'Разметка сайта',
      requiresAuth: true
    }
  },
  PageShortcodeCategories: {
    path: '/shortcodes/categories-page',
    component: '@/modules/cms_shortcodes/client/src/editor/PageCategories.vue',
    meta: {
      title: 'Категории страниц',
      requiresAuth: true
    }
  },
  CreatePage: {
    path: '/shortcodes/create-page',
    component: '@/modules/cms_shortcodes/client/src/editor/CreatePage.vue',
    meta: {
      title: 'Создание страниц',
      requiresAuth: true
    }
  },
  Pages: {
    path: '/shortcodes/pages',
    component: '@/modules/cms_shortcodes/client/src/AllPages.vue',
    meta: {
      title: 'Страницы',
      requiresAuth: true
    }
  },
  TemplateEditor: {
    path: '/shortcodes/templates/:id?',
    component: '@/modules/cms_shortcodes/client/src/editor/TemplateEditor.vue',
    meta: {
      title: 'Редактор компонентов',
      requiresAuth: true
    }
  },
  CmsAnyDepthPage: {
    path: '/shortcodes/:parts(.*)+',
    component: '@/modules/cms_shortcodes/client/src/CmsPage.vue',
    meta: {
      public: true
    }
  }
}

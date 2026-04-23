import { defineStore } from 'pinia';

export const useThemeStore = defineStore('theme', {
  state: () => ({
    currentTheme: localStorage.getItem('theme') || 'light',
    themes: {
      light: {
        name: '纸页',
        backgroundColor: '#f8f1e7',
        textColor: '#312a22',
        primaryColor: '#8b6f52',
        secondaryColor: '#fbf4e9',
      },
      dark: {
        name: '夜读',
        backgroundColor: '#211b16',
        textColor: '#fffaf2',
        primaryColor: '#c49a6c',
        secondaryColor: '#332920',
      },
      blue: {
        name: '湖蓝',
        backgroundColor: '#edf5f4',
        textColor: '#263433',
        primaryColor: '#6f9290',
        secondaryColor: '#dcebea',
      },
      green: {
        name: '草木',
        backgroundColor: '#f2f5eb',
        textColor: '#2d3327',
        primaryColor: '#71865a',
        secondaryColor: '#e5ead8',
      }
    }
  }),
  
  getters: {
    getCurrentTheme: (state) => state.currentTheme,
    getThemeConfig: (state) => state.themes[state.currentTheme],
    getAllThemes: (state) => Object.keys(state.themes).map(key => ({
      id: key,
      name: state.themes[key].name,
      primaryColor: state.themes[key].primaryColor
    }))
  },
  
  actions: {
    setTheme(themeName) {
      if (this.themes[themeName]) {
        this.currentTheme = themeName;
        localStorage.setItem('theme', themeName);
        this.applyTheme();
      }
    },
    
    applyTheme() {
      const theme = this.themes[this.currentTheme];
      document.documentElement.style.setProperty('--background-color', theme.backgroundColor);
      document.documentElement.style.setProperty('--text-color', theme.textColor);
      document.documentElement.style.setProperty('--primary-color', theme.primaryColor);
      document.documentElement.style.setProperty('--secondary-color', theme.secondaryColor);
    },
    
    initTheme() {
      this.applyTheme();
    }
  }
});

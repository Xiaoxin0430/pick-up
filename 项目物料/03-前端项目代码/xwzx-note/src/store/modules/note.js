import { defineStore } from 'pinia'
import axios from 'axios'
import { apiConfig } from '../../config/api'

export const useNoteStore = defineStore('note', {
  state: () => ({
    noteList: [],
    noteDetail: {},
    categories: [],
    currentCategory: 1,
    loading: false,
    refreshing: false,
    finished: false,
    categoriesLoading: false
  }),
  
  actions: {
    // 获取随笔分类
    async getCategories() {
      if (this.categoriesLoading) return;
      
      this.categoriesLoading = true;
      
      try {
        // 调用API获取分类列表
        const response = await axios.get(`${apiConfig.baseURL}/api/note/categories`);
        
        if (response.data && response.data.code === 200) {
          // 设置分类数据
          this.categories = [...response.data.data, { id: 10, name: '更多' }];
          
          // 如果没有设置当前分类，则设置为第一个分类
          if (!this.currentCategory && this.categories.length > 0) {
            this.currentCategory = this.categories[0].id;
          }
        }
      } catch (error) {
        console.error('获取随笔分类失败:', error);
        // 设置默认分类，以防API请求失败
        this.categories = [
          { id: 1, name: '头条' },
          { id: 2, name: '社会' },
          { id: 3, name: '国内' },
          { id: 4, name: '国际' },
          { id: 5, name: '娱乐' },
          { id: 6, name: '体育' },
          { id: 7, name: '科技' }
        ];
      } finally {
        this.categoriesLoading = false;
      }
    },
    
    // 切换随笔分类
    changeCategory(categoryId) {
      this.currentCategory = categoryId
      this.noteList = []
      this.finished = false
      this.getNoteList()
    },
    
    // 获取随笔列表
    async getNoteList(isRefresh = false) {
      if (isRefresh) {
        this.refreshing = true
        this.noteList = []
        this.finished = false
      }
      
      this.loading = true
      
      try {
        // 使用API请求获取随笔列表
        const params = {
          categoryId: this.currentCategory,
          page: isRefresh ? 1 : Math.ceil(this.noteList.length / 10) + 1,
          pageSize: 10
        }
        
        // 在开发环境中，直接使用模拟数据
        // console.log('使用模拟随笔列表数据');
        
        // 生成模拟数据
        // const mockData = Array.from({ length: 10 }, (_, index) => ({
        //   id: isRefresh ? index + 1 : this.noteList.length + index + 1,
        //   title: `${this.getCategoryName(this.currentCategory)}随笔${isRefresh ? index + 1 : this.noteList.length + index + 1}`,
        //   description: `这是一条关于${this.getCategoryName(this.currentCategory)}的随笔简介，包含了随笔的主要内容和亮点。`,
        //   image: `https://picsum.photos/id/${Math.floor(Math.random() * 100)}/200/200`,
        //   author: '随笔',
        //   publishTime: new Date().toLocaleString(),
        //   categoryId: this.currentCategory,
        //   views: Math.floor(Math.random() * 10000)
        // }))
        
        // this.noteList = isRefresh ? mockData : [...this.noteList, ...mockData]
        
        // 模拟数据加载完成的逻辑
        // if (this.noteList.length >= 30) {
        //   this.finished = true
        // }
        
 
        // 实际项目中连接后端API的代码，暂时注释掉
        const response = await axios.get(`${apiConfig.baseURL}/api/note/list`, { params });
        
        if (response.data && response.data.code === 200) {
          const noteData = response.data.data.list;
          
          // 更新随笔列表
          this.noteList = isRefresh ? noteData : [...this.noteList, ...noteData];
          
          // 判断是否加载完成
          if (noteData.length < params.pageSize) {
            this.finished = true;
          }
        }

      } catch (error) {
        console.error('获取随笔列表失败:', error)
      } finally {
        this.loading = false
        this.refreshing = false
      }
    },
    
    // 获取随笔详情
    async getNoteDetail(id) {
      try {
        // 在开发环境中，使用模拟数据
        console.log('使用模拟随笔详情数据');
        

        // 实际项目中连接后端API的代码，取消注释即可使用
        const response = await axios.get(`${apiConfig.baseURL}/api/note/detail?id=${id}`);
        
        if (response.data && response.data.code === 200) {
          // 设置随笔详情数据
          this.noteDetail = response.data.data;
          return;
        } else {
          console.error('获取随笔详情失败: 接口返回错误');
          // 接口失败时使用模拟数据作为备选
        }

      } catch (error) {
        console.error('获取随笔详情失败:', error);
        // 接口失败时使用模拟数据作为备选
      } 
        // 查找已有列表中的随笔
//         const existingNote = this.noteList.find(item => item.id === Number(id))
        
//         if (existingNote) {
//           this.noteDetail = {
//             ...existingNote,
//             content: `这是${existingNote.title}的详细内容。这是一篇关于${this.getCategoryName(existingNote.categoryId)}的随笔记录，内容丰富详实。
            
// 随笔事件发生在最近，引起了广泛关注。多方消息人士透露，该事件的影响将持续一段时间。

// 专家表示，此类事件的出现有其必然性，也反映了当前社会的某些问题。我们应当理性看待，并从中吸取经验教训。

// 接下来，相关部门将会采取措施，确保类似事件不再发生。公众也应当提高警惕，增强自我保护意识。

// 这是随笔详情的第二段落，提供了更多背景信息和细节描述。

// 这是随笔详情的第三段落，包含了各方观点和评论。

// 这是随笔详情的最后一段，总结了事件的影响和未来展望。`,
//             relatedNote: Array.from({ length: 3 }, (_, i) => ({
//               id: 1000 + i,
//               title: `相关${this.getCategoryName(existingNote.categoryId)}随笔${i + 1}`,
//               image: `https://picsum.photos/id/${Math.floor(Math.random() * 100)}/200/200`
//             }))
//           }
//         } else {
//           // 如果列表中没有，则生成一个新的详情
//           const categoryId = this.currentCategory
//           this.noteDetail = {
//             id: Number(id),
//             title: `${this.getCategoryName(categoryId)}随笔${id}`,
//             description: `这是一条关于${this.getCategoryName(categoryId)}的随笔简介，包含了随笔的主要内容和亮点。`,
//             image: `https://picsum.photos/id/${Math.floor(Math.random() * 100)}/200/200`,
//             author: '随笔',
//             publishTime: new Date().toLocaleString(),
//             categoryId: categoryId,
//             views: Math.floor(Math.random() * 10000),
//             content: `这是${this.getCategoryName(categoryId)}随笔${id}的详细内容。这是一篇关于${this.getCategoryName(categoryId)}的随笔记录，内容丰富详实。
            
// 随笔事件发生在最近，引起了广泛关注。多方消息人士透露，该事件的影响将持续一段时间。

// 专家表示，此类事件的出现有其必然性，也反映了当前社会的某些问题。我们应当理性看待，并从中吸取经验教训。

// 接下来，相关部门将会采取措施，确保类似事件不再发生。公众也应当提高警惕，增强自我保护意识。

// 这是随笔详情的第二段落，提供了更多背景信息和细节描述。

// 这是随笔详情的第三段落，包含了各方观点和评论。

// 这是随笔详情的最后一段，总结了事件的影响和未来展望。`,
//             relatedNote: Array.from({ length: 3 }, (_, i) => ({
//               id: 1000 + i,
//               title: `相关${this.getCategoryName(categoryId)}随笔${i + 1}`,
//               image: `https://picsum.photos/id/${Math.floor(Math.random() * 100)}/200/200`
//             }))
//           }
//         }
//             content: `这是${this.getCategoryName(categoryId)}随笔${id}的详细内容。这是一篇关于${this.getCategoryName(categoryId)}的随笔记录，内容丰富详实。
            
// 随笔事件发生在最近，引起了广泛关注。多方消息人士透露，该事件的影响将持续一段时间。

// 专家表示，此类事件的出现有其必然性，也反映了当前社会的某些问题。我们应当理性看待，并从中吸取经验教训。

// 接下来，相关部门将会采取措施，确保类似事件不再发生。公众也应当提高警惕，增强自我保护意识。

// 这是随笔详情的第二段落，提供了更多背景信息和细节描述。

// 这是随笔详情的第三段落，包含了各方观点和评论。

// 这是随笔详情的最后一段，总结了事件的影响和未来展望。`,
//             relatedNote: Array.from({ length: 3 }, (_, i) => ({
//               id: 1000 + i,
//               title: `相关${this.getCategoryName(categoryId)}随笔${i + 1}`,
//               image: `https://picsum.photos/id/${Math.floor(Math.random() * 100)}/200/200`
//             }))
//           }
//         }
//       } catch (error) {
//         console.error('获取随笔详情失败:', error)
//       }
//     },
},
    // 切换随笔分类
    changeCategory(categoryId) {
      if (this.currentCategory !== categoryId) {
        this.currentCategory = categoryId
        this.noteList = []
        this.finished = false
        this.getNoteList(true)
      }
    },
    
    // 获取分类名称
    getCategoryName(categoryId) {
      const category = this.categories.find(item => item.id === categoryId)
      return category ? category.name : '未知'
    }
  }
})
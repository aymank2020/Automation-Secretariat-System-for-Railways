<template>
  <div class="min-h-screen bg-gray-100 p-4">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="bg-gradient-to-r from-blue-600 to-blue-500 text-white p-4 rounded-t-lg">
        <h1 class="text-2xl font-bold text-center">البحث في الصادر</h1>
      </div>
      
      <div class="bg-white rounded-b-lg shadow-lg p-6">
        <!-- Search Form -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-1">رقم القيد</label>
            <input 
              v-model="search.qaid_number" 
              type="text" 
              class="w-full border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-1">رقم الخطاب</label>
            <input 
              v-model="search.letter_number" 
              type="text" 
              class="w-full border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-1">الموضوع</label>
            <input 
              v-model="search.subject" 
              type="text" 
              class="w-full border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-1">الإدارة</label>
            <input 
              v-model="search.source_administration" 
              type="text" 
              class="w-full border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-1">من تاريخ</label>
            <input 
              v-model="search.date_from" 
              type="date" 
              class="w-full border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-1">إلى تاريخ</label>
            <input 
              v-model="search.date_to" 
              type="date" 
              class="w-full border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-1">حالة التوقيع</label>
            <select 
              v-model="search.signature_status" 
              class="w-full border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-500"
            >
              <option value="">الكل</option>
              <option value="pending">انتظار</option>
              <option value="saved">حفظ</option>
            </select>
          </div>
          <div class="flex items-end">
            <button 
              @click="performSearch"
              class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded font-bold transition"
            >
              بحث
            </button>
          </div>
        </div>
        
        <!-- Results Table -->
        <div class="overflow-x-auto">
          <table class="w-full border-collapse border border-gray-300">
            <thead>
              <tr class="bg-gray-100">
                <th class="border border-gray-300 px-4 py-2 text-right">رقم القيد</th>
                <th class="border border-gray-300 px-4 py-2 text-right">تاريخ القيد</th>
                <th class="border border-gray-300 px-4 py-2 text-right">رقم الخطاب</th>
                <th class="border border-gray-300 px-4 py-2 text-right">الموضوع</th>
                <th class="border border-gray-300 px-4 py-2 text-right">الإدارة</th>
                <th class="border border-gray-300 px-4 py-2 text-right">حالة التوقيع</th>
                <th class="border border-gray-300 px-4 py-2 text-center">إجراءات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading" class="text-center">
                <td colspan="7" class="border border-gray-300 px-4 py-8">
                  <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                </td>
              </tr>
              <tr v-else-if="results.length === 0" class="text-center">
                <td colspan="7" class="border border-gray-300 px-4 py-8 text-gray-500">
                  لا توجد نتائج
                </td>
              </tr>
              <tr v-for="item in results" :key="item.id" class="hover:bg-gray-50">
                <td class="border border-gray-300 px-4 py-2">{{ item.qaid_number }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ formatDate(item.qaid_date) }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ item.letter_number || '-' }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ item.subject }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ item.source_administration || '-' }}</td>
                <td class="border border-gray-300 px-4 py-2">
                  <span :class="{
                    'text-yellow-600': item.signature_status === 'pending',
                    'text-green-600': item.signature_status === 'saved'
                  }">
                    {{ item.signature_status === 'pending' ? 'انتظار' : 'حفظ' }}
                  </span>
                </td>
                <td class="border border-gray-300 px-4 py-2 text-center">
                  <button 
                    @click="editItem(item.id)"
                    class="text-blue-600 hover:text-blue-800 mx-1"
                    title="تعديل"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                  </button>
                  <button 
                    @click="deleteItem(item.id)"
                    class="text-red-600 hover:text-red-800 mx-1"
                    title="حذف"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- Action Buttons -->
        <div class="flex justify-center gap-4 mt-6">
          <button 
            @click="$router.push('/home')"
            class="bg-gradient-to-r from-red-500 to-red-400 hover:from-red-600 hover:to-red-500 text-white px-8 py-3 rounded-lg font-bold transition"
          >
            خروج
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const loading = ref(false)
const results = ref([])

const search = ref({
  qaid_number: '',
  letter_number: '',
  subject: '',
  source_administration: '',
  date_from: '',
  date_to: '',
  signature_status: ''
})

async function performSearch() {
  loading.value = true
  try {
    const token = localStorage.getItem('token')
    const params = {}
    
    if (search.value.qaid_number) params.qaid_number = search.value.qaid_number
    if (search.value.subject) params.subject = search.value.subject
    if (search.value.date_from) params.date_from = search.value.date_from
    if (search.value.date_to) params.date_to = search.value.date_to
    
    const response = await axios.get(`${API_URL}/sadir/`, {
      headers: { Authorization: `Bearer ${token}` },
      params
    })
    
    results.value = response.data
  } catch (error) {
    console.error('Error searching:', error)
    alert('خطأ في البحث')
  } finally {
    loading.value = false
  }
}

function editItem(id) {
  router.push(`/sadir/${id}/edit`)
}

async function deleteItem(id) {
  if (!confirm('هل أنت متأكد من الحذف؟')) return
  
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`${API_URL}/sadir/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    alert('تم الحذف بنجاح')
    performSearch()
  } catch (error) {
    console.error('Error deleting:', error)
    alert('خطأ في الحذف')
  }
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('ar-EG')
}

onMounted(() => {
  performSearch()
})
</script>

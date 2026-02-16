<template>
  <div class="min-h-screen bg-gray-100 p-4">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="bg-gradient-to-r from-blue-600 to-blue-500 text-white p-4 rounded-t-lg">
        <h1 class="text-2xl font-bold text-center">استعلام في الصادر</h1>
      </div>
      
      <div class="bg-white rounded-b-lg shadow-lg p-6">
        <!-- Quick Search -->
        <div class="flex gap-4 mb-6">
          <input 
            v-model="quickSearch" 
            type="text" 
            placeholder="بحث سريع (رقم القيد، رقم الخطاب، الموضوع، الإدارة...)"
            class="flex-1 border border-gray-300 rounded px-4 py-3 focus:ring-2 focus:ring-blue-500"
            @keyup.enter="performQuickSearch"
          />
          <button 
            @click="performQuickSearch"
            class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded font-bold transition"
          >
            بحث
          </button>
        </div>
        
        <!-- Statistics -->
        <div class="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
          <div class="bg-blue-50 rounded-lg p-4 text-center">
            <p class="text-gray-600 text-sm">إجمالي الصادر</p>
            <p class="text-3xl font-bold text-blue-600">{{ stats.total }}</p>
          </div>
          <div class="bg-yellow-50 rounded-lg p-4 text-center">
            <p class="text-gray-600 text-sm">في الانتظار</p>
            <p class="text-3xl font-bold text-yellow-600">{{ stats.pending }}</p>
          </div>
          <div class="bg-green-50 rounded-lg p-4 text-center">
            <p class="text-gray-600 text-sm">تم الحفظ</p>
            <p class="text-3xl font-bold text-green-600">{{ stats.saved }}</p>
          </div>
          <div class="bg-red-50 rounded-lg p-4 text-center">
            <p class="text-gray-600 text-sm">يحتاج متابعة</p>
            <p class="text-3xl font-bold text-red-600">{{ stats.needs_followup }}</p>
          </div>
          <div class="bg-purple-50 rounded-lg p-4 text-center">
            <p class="text-gray-600 text-sm">موقع من الرئيس</p>
            <p class="text-3xl font-bold text-purple-600">{{ stats.signed_by_chief }}</p>
          </div>
        </div>
        
        <!-- Results Table -->
        <div class="overflow-x-auto">
          <table class="w-full border-collapse border border-gray-300">
            <thead>
              <tr class="bg-gray-100">
                <th class="border border-gray-300 px-4 py-2 text-right">رقم القيد</th>
                <th class="border border-gray-300 px-4 py-2 text-right">رقم الخطاب</th>
                <th class="border border-gray-300 px-4 py-2 text-right">الموضوع</th>
                <th class="border border-gray-300 px-4 py-2 text-right">الإدارة</th>
                <th class="border border-gray-300 px-4 py-2 text-right">التاريخ</th>
                <th class="border border-gray-300 px-4 py-2 text-right">الحالة</th>
                <th class="border border-gray-300 px-4 py-2 text-center">تفاصيل</th>
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
                <td class="border border-gray-300 px-4 py-2">{{ item.letter_number || '-' }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ item.subject }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ item.source_administration || '-' }}</td>
                <td class="border border-gray-300 px-4 py-2">{{ formatDate(item.qaid_date) }}</td>
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
                    @click="showDetails(item)"
                    class="text-blue-600 hover:text-blue-800"
                    title="عرض التفاصيل"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
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
    
    <!-- Details Modal -->
    <div v-if="selectedItem" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-auto">
        <div class="p-6">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-bold">تفاصيل الصادر</h2>
            <button @click="selectedItem = null" class="text-gray-500 hover:text-gray-700">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
          <div class="space-y-2 text-sm">
            <div class="grid grid-cols-2 gap-4">
              <div><span class="font-bold">رقم القيد:</span> {{ selectedItem.qaid_number }}</div>
              <div><span class="font-bold">تاريخ القيد:</span> {{ formatDate(selectedItem.qaid_date) }}</div>
              <div><span class="font-bold">الإدارة الوارد منها:</span> {{ selectedItem.source_administration || '-' }}</div>
              <div><span class="font-bold">رقم الخطاب:</span> {{ selectedItem.letter_number || '-' }}</div>
              <div><span class="font-bold">تاريخ الخطاب:</span> {{ formatDate(selectedItem.letter_date) }}</div>
              <div><span class="font-bold">عدد المرفقات:</span> {{ selectedItem.attachment_count || 0 }}</div>
              <div class="col-span-2"><span class="font-bold">الموضوع:</span> {{ selectedItem.subject }}</div>
              <div><span class="font-bold">حالة التوقيع:</span> {{ selectedItem.signature_status === 'pending' ? 'انتظار' : 'حفظ' }}</div>
              <div><span class="font-bold">تاريخ التوقيع:</span> {{ formatDate(selectedItem.signature_date) }}</div>
              <div><span class="font-bold">الوزارة:</span> {{ selectedItem.is_ministry ? 'نعم' : 'لا' }}</div>
              <div><span class="font-bold">الهيئة:</span> {{ selectedItem.is_authority ? 'نعم' : 'لا' }}</div>
              <div><span class="font-bold">جهة أخرى:</span> {{ selectedItem.is_other ? 'نعم' : 'لا' }}</div>
              <div><span class="font-bold">موقع من الرئيس:</span> {{ selectedItem.signed_by_chief ? 'نعم' : 'لا' }}</div>
              <div><span class="font-bold">تم تصديرها إلى:</span> {{ selectedItem.exported_to || '-' }}</div>
              <div><span class="font-bold">تاريخ التصدير:</span> {{ formatDate(selectedItem.export_date) }}</div>
              <div><span class="font-bold">يحتاج متابعة:</span> {{ selectedItem.needs_followup ? 'نعم' : 'لا' }}</div>
              <div class="col-span-2"><span class="font-bold">ملاحظات:</span> {{ selectedItem.notes || '-' }}</div>
            </div>
          </div>
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
const quickSearch = ref('')
const selectedItem = ref(null)

const stats = ref({
  total: 0,
  pending: 0,
  saved: 0,
  needs_followup: 0,
  signed_by_chief: 0
})

async function performQuickSearch() {
  if (!quickSearch.value.trim()) {
    loadAll()
    return
  }
  
  loading.value = true
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`${API_URL}/sadir/search`, {
      headers: { Authorization: `Bearer ${token}` },
      params: { q: quickSearch.value }
    })
    
    results.value = response.data
  } catch (error) {
    console.error('Error searching:', error)
    alert('خطأ في البحث')
  } finally {
    loading.value = false
  }
}

async function loadAll() {
  loading.value = true
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`${API_URL}/sadir/`, {
      headers: { Authorization: `Bearer ${token}` },
      params: { limit: 50 }
    })
    
    results.value = response.data
  } catch (error) {
    console.error('Error loading:', error)
  } finally {
    loading.value = false
  }
}

async function loadStats() {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`${API_URL}/sadir/stats/summary`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    stats.value = response.data
  } catch (error) {
    console.error('Error loading stats:', error)
  }
}

function showDetails(item) {
  selectedItem.value = item
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('ar-EG')
}

onMounted(() => {
  loadAll()
  loadStats()
})
</script>

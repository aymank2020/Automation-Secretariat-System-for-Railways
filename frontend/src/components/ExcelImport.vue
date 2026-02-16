<template>
  <div class="bg-white rounded-lg shadow-lg p-6">
    <h2 class="text-xl font-bold mb-4">استيراد من Excel</h2>
    
    <!-- Document Type Selection -->
    <div class="mb-4">
      <label class="block text-sm font-bold text-gray-700 mb-2">نوع البيانات</label>
      <div class="flex gap-4">
        <label class="flex items-center gap-2">
          <input v-model="docType" type="radio" value="warid" class="w-4 h-4" />
          <span>وارد</span>
        </label>
        <label class="flex items-center gap-2">
          <input v-model="docType" type="radio" value="sadir" class="w-4 h-4" />
          <span>صادر</span>
        </label>
      </div>
    </div>
    
    <!-- File Upload -->
    <div class="mb-4">
      <label class="block text-sm font-bold text-gray-700 mb-2">ملف Excel</label>
      <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
        <input 
          ref="fileInput"
          type="file" 
          @change="handleFileChange"
          accept=".xlsx,.xls,.csv"
          class="hidden"
        />
        <button 
          type="button"
          @click="$refs.fileInput.click()"
          class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-bold transition"
        >
          اختيار ملف
        </button>
        <p class="text-gray-500 mt-2">Excel, CSV (حد أقصى 10MB)</p>
        <p v-if="selectedFile" class="mt-2 text-blue-600 font-bold">{{ selectedFile.name }}</p>
      </div>
    </div>
    
    <!-- Preview -->
    <div v-if="previewData.length > 0" class="mb-4">
      <h3 class="text-lg font-bold mb-2">معاينة البيانات (أول 5 صفوف)</h3>
      <div class="overflow-x-auto">
        <table class="w-full border-collapse border border-gray-300 text-sm">
          <thead>
            <tr class="bg-gray-100">
              <th v-for="col in previewColumns" :key="col" class="border border-gray-300 px-3 py-2">
                {{ col }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in previewData" :key="index">
              <td v-for="col in previewColumns" :key="col" class="border border-gray-300 px-3 py-2">
                {{ row[col] }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <p class="text-gray-600 mt-2">إجمالي الصفوف: {{ totalRows }}</p>
    </div>
    
    <!-- Actions -->
    <div class="flex gap-4">
      <button 
        @click="previewFile"
        :disabled="!selectedFile || loadingPreview"
        class="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded font-bold transition disabled:opacity-50"
      >
        <span v-if="loadingPreview">جاري المعاينة...</span>
        <span v-else>معاينة</span>
      </button>
      <button 
        @click="importFile"
        :disabled="!selectedFile || previewData.length === 0 || loadingImport"
        class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded font-bold transition disabled:opacity-50"
      >
        <span v-if="loadingImport">جاري الاستيراد...</span>
        <span v-else>استيراد</span>
      </button>
    </div>
    
    <!-- Results -->
    <div v-if="importResult" class="mt-4 p-4 rounded-lg" :class="importResult.success ? 'bg-green-100' : 'bg-red-100'">
      <p class="font-bold">{{ importResult.message }}</p>
      <p v-if="importResult.imported_count">تم استيراد: {{ importResult.imported_count }} سجل</p>
      <p v-if="importResult.errors && importResult.errors.length > 0" class="text-red-600 mt-2">
        أخطاء: {{ importResult.errors.length }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const docType = ref('warid')
const selectedFile = ref(null)
const previewData = ref([])
const previewColumns = ref([])
const totalRows = ref(0)
const loadingPreview = ref(false)
const loadingImport = ref(false)
const importResult = ref(null)

function handleFileChange(event) {
  const file = event.target.files[0]
  if (file) {
    if (file.size > 10 * 1024 * 1024) {
      alert('حجم الملف كبير جداً. الحد الأقصى 10MB')
      return
    }
    selectedFile.value = file
    previewData.value = []
    importResult.value = null
  }
}

async function previewFile() {
  if (!selectedFile.value) return
  
  loadingPreview.value = true
  try {
    const token = localStorage.getItem('token')
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    
    const response = await axios.post(`${API_URL}/import/${docType.value}/preview`, formData, {
      headers: { 
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    
    previewData.value = response.data.preview_data
    previewColumns.value = response.data.columns
    totalRows.value = response.data.total_rows
  } catch (error) {
    console.error('Error previewing:', error)
    alert('خطأ في معاينة الملف: ' + (error.response?.data?.detail || error.message))
  } finally {
    loadingPreview.value = false
  }
}

async function importFile() {
  if (!selectedFile.value) return
  
  loadingImport.value = true
  try {
    const token = localStorage.getItem('token')
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    
    const response = await axios.post(`${API_URL}/import/${docType.value}`, formData, {
      headers: { 
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    
    importResult.value = response.data
  } catch (error) {
    console.error('Error importing:', error)
    importResult.value = {
      success: false,
      message: 'خطأ في الاستيراد: ' + (error.response?.data?.detail || error.message)
    }
  } finally {
    loadingImport.value = false
  }
}
</script>

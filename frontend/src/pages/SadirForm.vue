<template>
  <div class="min-h-screen bg-gray-100 p-4">
    <div class="max-w-6xl mx-auto bg-white rounded-lg shadow-lg overflow-hidden">
      <!-- Header -->
      <div class="bg-gradient-to-r from-blue-600 to-blue-500 text-white p-4">
        <h1 class="text-2xl font-bold text-center">خطابات الصادر</h1>
      </div>
      
      <div class="p-6">
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <!-- Row 1: رقم القيد وتاريخ القيد -->
          <div class="grid grid-cols-4 gap-4 items-center">
            <div class="col-span-1 text-right">
              <label class="font-bold text-gray-700">رقم القيد :</label>
            </div>
            <div class="col-span-1">
              <input 
                v-model="form.qaid_number" 
                type="text" 
                class="w-full border border-gray-300 rounded px-3 py-2 text-center focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>
            <div class="col-span-1 text-right">
              <label class="font-bold text-gray-700">تاريخ القيد :</label>
            </div>
            <div class="col-span-1">
              <input 
                v-model="form.qaid_date" 
                type="date" 
                class="w-full border border-gray-300 rounded px-3 py-2 text-center focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>
          </div>
          
          <!-- Row 2: الإدارة الوارد منها ورقم الخطاب وتاريخ الخطاب -->
          <div class="grid grid-cols-6 gap-4 items-center">
            <div class="col-span-2 text-right">
              <label class="font-bold text-gray-700">الإدارة الوارد منها :</label>
            </div>
            <div class="col-span-1">
              <input 
                v-model="form.source_administration" 
                type="text" 
                class="w-full border border-gray-300 rounded px-3 py-2 text-center focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div class="col-span-1 text-right">
              <label class="font-bold text-gray-700">رقم الخطاب :</label>
            </div>
            <div class="col-span-1">
              <input 
                v-model="form.letter_number" 
                type="text" 
                class="w-full border border-gray-300 rounded px-3 py-2 text-center focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div class="col-span-1">
              <input 
                v-model="form.letter_date" 
                type="date" 
                class="w-full border border-gray-300 rounded px-3 py-2 text-center focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          
          <!-- Row 3: عدد المرفقات والموضوع -->
          <div class="grid grid-cols-12 gap-4 items-start">
            <div class="col-span-2 text-right">
              <label class="font-bold text-gray-700">عدد المرفقات :</label>
            </div>
            <div class="col-span-1">
              <input 
                v-model="form.attachment_count" 
                type="number" 
                min="0"
                class="w-full border border-gray-300 rounded px-3 py-2 text-center focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div class="col-span-1 text-right">
              <label class="font-bold text-gray-700">الموضوع :</label>
            </div>
            <div class="col-span-8">
              <textarea 
                v-model="form.subject" 
                rows="3"
                class="w-full border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-500"
                required
              ></textarea>
            </div>
          </div>
          
          <!-- Row 4: تم التوقيع -->
          <div class="grid grid-cols-12 gap-2 items-center">
            <div class="col-span-1 text-right">
              <label class="font-bold text-gray-700">تم التوقيع :</label>
            </div>
            <div class="col-span-2 flex items-center gap-4">
              <label class="flex items-center gap-2">
                <input v-model="form.signature_status" type="radio" value="pending" class="w-4 h-4" />
                <span>انتظار</span>
              </label>
              <label class="flex items-center gap-2">
                <input v-model="form.signature_status" type="radio" value="saved" class="w-4 h-4" />
                <span>حفظ</span>
              </label>
            </div>
            <div class="col-span-2 text-right">
              <label class="font-bold text-gray-700">تاريخ التوقيع :</label>
            </div>
            <div class="col-span-2">
              <input 
                v-model="form.signature_date" 
                type="date" 
                class="w-full border border-gray-300 rounded px-3 py-2 text-center focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          
          <!-- Row 5: صادر إلى (3 rows) -->
          <div class="space-y-2">
            <div v-for="i in 3" :key="i" class="grid grid-cols-12 gap-2 items-center">
              <div class="col-span-1 text-right">
                <label class="font-bold text-gray-700">صادر إلى :</label>
              </div>
              <div class="col-span-3">
                <input 
                  v-model="form['recipient_' + i + '_name']" 
                  type="text" 
                  class="w-full border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-500"
                  :placeholder="'اسم المستلم ' + i"
                />
              </div>
              <div class="col-span-2 text-right">
                <label class="font-bold text-gray-700">تاريخ التسليم :</label>
              </div>
              <div class="col-span-2">
                <input 
                  v-model="form['recipient_' + i + '_delivery_date']" 
                  type="date" 
                  class="w-full border border-gray-300 rounded px-3 py-2 text-center focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div class="col-span-2 text-right" v-if="i === 1">
                <label class="font-bold text-gray-700">اسم المستلم :</label>
              </div>
              <div class="col-span-2" v-if="i === 1">
                <input 
                  v-model="form.recipient_1_name" 
                  type="text" 
                  class="w-full border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
          </div>
          
          <!-- Row 6: الوزارة/الهيئة/جهة أخرى -->
          <div class="grid grid-cols-12 gap-4 items-center">
            <div class="col-span-1 text-right">
              <label class="font-bold text-gray-700">الوزارة :</label>
            </div>
            <div class="col-span-1">
              <input v-model="form.is_ministry" type="checkbox" class="w-5 h-5" />
            </div>
            <div class="col-span-1 text-right">
              <label class="font-bold text-gray-700">الهيئة :</label>
            </div>
            <div class="col-span-1">
              <input v-model="form.is_authority" type="checkbox" class="w-5 h-5" />
            </div>
            <div class="col-span-1 text-right">
              <label class="font-bold text-gray-700">جهة أخرى :</label>
            </div>
            <div class="col-span-1">
              <input v-model="form.is_other" type="checkbox" class="w-5 h-5" />
            </div>
            <div class="col-span-2 text-right">
              <label class="font-bold text-gray-700">اسم ملف الحفظ :</label>
            </div>
            <div class="col-span-2">
              <input 
                v-model="form.file_name" 
                type="text" 
                class="w-full border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div class="col-span-1 text-right">
              <label class="font-bold text-gray-700">يحتاج لمتابعة :</label>
            </div>
            <div class="col-span-1">
              <select 
                v-model="form.needs_followup" 
                class="w-full border border-gray-300 rounded px-2 py-2 focus:ring-2 focus:ring-blue-500"
              >
                <option :value="false">No</option>
                <option :value="true">Yes</option>
              </select>
            </div>
          </div>
          
          <!-- Row 7: توقيع رئيس الهيئة -->
          <div class="grid grid-cols-12 gap-4 items-center">
            <div class="col-span-3 text-right">
              <label class="font-bold text-gray-700">تم التوقيع من رئيس الهيئة :</label>
            </div>
            <div class="col-span-1">
              <select 
                v-model="form.signed_by_chief" 
                class="w-full border border-gray-300 rounded px-2 py-2 focus:ring-2 focus:ring-blue-500"
              >
                <option :value="false">No</option>
                <option :value="true">Yes</option>
              </select>
            </div>
            <div class="col-span-2 text-right">
              <label class="font-bold text-gray-700">تم تصديرها إلى :</label>
            </div>
            <div class="col-span-2">
              <input 
                v-model="form.exported_to" 
                type="text" 
                class="w-full border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div class="col-span-2 text-right">
              <label class="font-bold text-gray-700">تاريخ التصدير :</label>
            </div>
            <div class="col-span-2">
              <input 
                v-model="form.export_date" 
                type="date" 
                class="w-full border border-gray-300 rounded px-3 py-2 text-center focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          
          <!-- Row 8: نوع الخطاب ومرتبط بخطاب آخر -->
          <div class="grid grid-cols-8 gap-4 items-center">
            <div class="col-span-1 text-right">
              <label class="font-bold text-gray-700">نوع الخطاب :</label>
            </div>
            <div class="col-span-1">
              <select 
                v-model="form.letter_type" 
                class="w-full border border-gray-300 rounded px-2 py-2 focus:ring-2 focus:ring-blue-500"
              >
                <option value="">اختر...</option>
                <option value="official">رسمي</option>
                <option value="internal">داخلي</option>
                <option value="external">خارجي</option>
                <option value="urgent">عاجل</option>
              </select>
            </div>
            <div class="col-span-2 text-right">
              <label class="font-bold text-gray-700">مرتبط بخطاب آخر :</label>
            </div>
            <div class="col-span-1">
              <select 
                v-model="form.linked_to_another" 
                class="w-full border border-gray-300 rounded px-2 py-2 focus:ring-2 focus:ring-blue-500"
              >
                <option :value="false">No</option>
                <option :value="true">Yes</option>
              </select>
            </div>
            <div class="col-span-1 text-right">
              <label class="font-bold text-gray-700">صورة الخطاب :</label>
            </div>
            <div class="col-span-2">
              <div class="border-2 border-dashed border-gray-300 rounded-lg p-2 text-center">
                <input 
                  ref="fileInput"
                  type="file" 
                  @change="handleFileChange"
                  accept=".pdf,.jpg,.jpeg,.png"
                  class="hidden"
                />
                <button 
                  type="button"
                  @click="$refs.fileInput.click()"
                  class="bg-gray-200 hover:bg-gray-300 px-3 py-1 rounded text-sm transition"
                >
                  اختيار ملف
                </button>
                <p v-if="selectedFile" class="mt-1 text-xs text-blue-600">{{ selectedFile.name }}</p>
              </div>
            </div>
          </div>
          
          <!-- Row 9: رقم قيد الخطاب الآخر وملاحظات -->
          <div class="grid grid-cols-12 gap-4 items-start">
            <div class="col-span-2 text-right">
              <label class="font-bold text-gray-700">رقم قيد الخطاب الآخر :</label>
            </div>
            <div class="col-span-2">
              <input 
                v-model="form.other_letter_qaid" 
                type="text" 
                class="w-full border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-500"
                :disabled="!form.linked_to_another"
              />
            </div>
            <div class="col-span-1 text-right">
              <label class="font-bold text-gray-700">ملاحظات :</label>
            </div>
            <div class="col-span-7">
              <textarea 
                v-model="form.notes" 
                rows="3"
                class="w-full border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-500"
              ></textarea>
            </div>
          </div>
          
          <!-- Action Buttons -->
          <div class="flex justify-center gap-4 pt-6 border-t">
            <button 
              type="submit" 
              :disabled="loading"
              class="bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600 text-white px-8 py-3 rounded-lg font-bold transition flex items-center gap-2 disabled:opacity-50"
            >
              <svg v-if="loading" class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span v-else>{{ isEdit ? 'تحديث' : 'حفظ' }}</span>
            </button>
            <button 
              type="button"
              @click="resetForm"
              class="bg-gradient-to-r from-gray-500 to-gray-400 hover:from-gray-600 hover:to-gray-500 text-white px-8 py-3 rounded-lg font-bold transition"
            >
              جديد
            </button>
            <button 
              type="button"
              @click="$router.push('/home')"
              class="bg-gradient-to-r from-red-500 to-red-400 hover:from-red-600 hover:to-red-500 text-white px-8 py-3 rounded-lg font-bold transition"
            >
              خروج
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const isEdit = computed(() => !!route.params.id)
const loading = ref(false)
const selectedFile = ref(null)
const fileInput = ref(null)

const form = ref({
  qaid_number: '',
  qaid_date: new Date().toISOString().split('T')[0],
  source_administration: '',
  letter_number: '',
  letter_date: '',
  attachment_count: 0,
  subject: '',
  signature_status: 'pending',
  signature_date: '',
  recipient_1_name: '',
  recipient_1_delivery_date: '',
  recipient_2_name: '',
  recipient_2_delivery_date: '',
  recipient_3_name: '',
  recipient_3_delivery_date: '',
  is_ministry: false,
  is_authority: false,
  is_other: false,
  file_name: '',
  needs_followup: false,
  signed_by_chief: false,
  exported_to: '',
  export_date: '',
  letter_type: '',
  linked_to_another: false,
  other_letter_qaid: '',
  notes: ''
})

function handleFileChange(event) {
  const file = event.target.files[0]
  if (file) {
    if (file.size > 5 * 1024 * 1024) {
      alert('حجم الملف كبير جداً. الحد الأقصى 5MB')
      return
    }
    selectedFile.value = file
  }
}

async function handleSubmit() {
  loading.value = true
  try {
    const token = localStorage.getItem('token')
    const headers = { Authorization: `Bearer ${token}` }
    
    if (isEdit.value) {
      await axios.put(`${API_URL}/sadir/${route.params.id}`, form.value, { headers })
    } else {
      const response = await axios.post(`${API_URL}/sadir/`, form.value, { headers })
      
      // رفع الملف إذا تم اختياره
      if (selectedFile.value && response.data.id) {
        const formData = new FormData()
        formData.append('file', selectedFile.value)
        await axios.post(`${API_URL}/sadir/${response.data.id}/upload`, formData, { 
          headers: { ...headers, 'Content-Type': 'multipart/form-data' }
        })
      }
    }
    
    alert(isEdit.value ? 'تم التحديث بنجاح' : 'تم الحفظ بنجاح')
    if (!isEdit.value) {
      resetForm()
    }
  } catch (error) {
    console.error('Error:', error)
    alert('حدث خطأ: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

function resetForm() {
  form.value = {
    qaid_number: '',
    qaid_date: new Date().toISOString().split('T')[0],
    source_administration: '',
    letter_number: '',
    letter_date: '',
    attachment_count: 0,
    subject: '',
    signature_status: 'pending',
    signature_date: '',
    recipient_1_name: '',
    recipient_1_delivery_date: '',
    recipient_2_name: '',
    recipient_2_delivery_date: '',
    recipient_3_name: '',
    recipient_3_delivery_date: '',
    is_ministry: false,
    is_authority: false,
    is_other: false,
    file_name: '',
    needs_followup: false,
    signed_by_chief: false,
    exported_to: '',
    export_date: '',
    letter_type: '',
    linked_to_another: false,
    other_letter_qaid: '',
    notes: ''
  }
  selectedFile.value = null
}

async function loadSadir() {
  if (!isEdit.value) return
  
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`${API_URL}/sadir/${route.params.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    const data = response.data
    form.value = {
      ...data,
      qaid_date: data.qaid_date ? data.qaid_date.split('T')[0] : '',
      letter_date: data.letter_date ? data.letter_date.split('T')[0] : '',
      signature_date: data.signature_date ? data.signature_date.split('T')[0] : '',
      export_date: data.export_date ? data.export_date.split('T')[0] : '',
      recipient_1_delivery_date: data.recipient_1_delivery_date ? data.recipient_1_delivery_date.split('T')[0] : '',
      recipient_2_delivery_date: data.recipient_2_delivery_date ? data.recipient_2_delivery_date.split('T')[0] : '',
      recipient_3_delivery_date: data.recipient_3_delivery_date ? data.recipient_3_delivery_date.split('T')[0] : ''
    }
  } catch (error) {
    console.error('Error loading sadir:', error)
    alert('خطأ في تحميل البيانات')
  }
}

onMounted(() => {
  loadSadir()
})
</script>

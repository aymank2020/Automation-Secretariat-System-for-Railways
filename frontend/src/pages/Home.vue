<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-5xl">
      <!-- Header with logos -->
      <div class="flex justify-between items-start mb-6">
        <!-- Left Logo -->
        <div class="text-center">
          <div class="w-24 h-24 bg-blue-900 rounded-full flex items-center justify-center mb-2">
            <span class="text-white text-2xl font-bold">هـ.ق</span>
          </div>
          <p class="text-xs text-blue-900 font-bold text-center leading-tight">
            الهيئة القومية<br>لسكك حديد مصر
          </p>
        </div>
        
        <!-- Title -->
        <div class="text-center flex-1 mx-8">
          <div class="bg-gradient-to-r from-blue-800 to-blue-600 text-white py-3 px-8 rounded-lg mb-2">
            <h1 class="text-3xl font-bold">الصادر والوارد</h1>
          </div>
          <div class="bg-gradient-to-r from-blue-700 to-blue-500 text-white py-2 px-8 rounded-lg">
            <h2 class="text-xl font-bold">قطاع الموارد البشرية</h2>
          </div>
        </div>
        
        <!-- Right Logo -->
        <div class="text-center">
          <div class="w-24 h-24 bg-blue-900 rounded-full flex items-center justify-center mb-2">
            <span class="text-white text-2xl font-bold">هـ.ق</span>
          </div>
          <p class="text-xs text-blue-900 font-bold text-center leading-tight">
            الهيئة القومية<br>لسكك حديد مصر
          </p>
        </div>
      </div>
      
      <!-- Main Logo -->
      <div class="flex justify-center mb-8">
        <div class="w-32 h-32 border-4 border-blue-900 rounded-full flex items-center justify-center bg-white">
          <div class="text-center">
            <svg class="w-16 h-16 mx-auto text-blue-900" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
            </svg>
            <p class="text-xs text-blue-900 font-bold mt-1">Egyptian Railways</p>
          </div>
        </div>
      </div>
      
      <!-- Buttons Grid -->
      <div class="grid grid-cols-2 gap-8 mb-8">
        <!-- Incoming Section -->
        <div class="space-y-4">
          <button 
            @click="$router.push('/warid/new')" 
            class="w-full bg-gradient-to-r from-blue-100 to-blue-200 hover:from-blue-200 hover:to-blue-300 text-blue-900 py-4 rounded-lg font-bold text-lg transition-all duration-300 shadow-md hover:shadow-lg border-2 border-blue-300"
          >
            <span class="flex items-center justify-center gap-2">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"/>
              </svg>
              أدخال الوارد
            </span>
          </button>
          <button 
            @click="$router.push('/warid/search')" 
            class="w-full bg-gradient-to-r from-blue-100 to-blue-200 hover:from-blue-200 hover:to-blue-300 text-blue-900 py-4 rounded-lg font-bold text-lg transition-all duration-300 shadow-md hover:shadow-lg border-2 border-blue-300"
          >
            <span class="flex items-center justify-center gap-2">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
              بحث في الوارد
            </span>
          </button>
          <button 
            @click="$router.push('/warid/query')" 
            class="w-full bg-gradient-to-r from-blue-100 to-blue-200 hover:from-blue-200 hover:to-blue-300 text-blue-900 py-4 rounded-lg font-bold text-lg transition-all duration-300 shadow-md hover:shadow-lg border-2 border-blue-300"
          >
            <span class="flex items-center justify-center gap-2">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
              </svg>
              استعلام في الوارد
            </span>
          </button>
        </div>
        
        <!-- Outgoing Section -->
        <div class="space-y-4">
          <button 
            @click="$router.push('/sadir/new')" 
            class="w-full bg-gradient-to-r from-blue-100 to-blue-200 hover:from-blue-200 hover:to-blue-300 text-blue-900 py-4 rounded-lg font-bold text-lg transition-all duration-300 shadow-md hover:shadow-lg border-2 border-blue-300"
          >
            <span class="flex items-center justify-center gap-2">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
              </svg>
              أدخال الصادر
            </span>
          </button>
          <button 
            @click="$router.push('/sadir/search')" 
            class="w-full bg-gradient-to-r from-blue-100 to-blue-200 hover:from-blue-200 hover:to-blue-300 text-blue-900 py-4 rounded-lg font-bold text-lg transition-all duration-300 shadow-md hover:shadow-lg border-2 border-blue-300"
          >
            <span class="flex items-center justify-center gap-2">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
              بحث في الصادر
            </span>
          </button>
          <button 
            @click="$router.push('/sadir/query')" 
            class="w-full bg-gradient-to-r from-blue-100 to-blue-200 hover:from-blue-200 hover:to-blue-300 text-blue-900 py-4 rounded-lg font-bold text-lg transition-all duration-300 shadow-md hover:shadow-lg border-2 border-blue-300"
          >
            <span class="flex items-center justify-center gap-2">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
              </svg>
              استعلام في الصادر
            </span>
          </button>
        </div>
      </div>
      
      <!-- Exit Button -->
      <div class="text-center">
        <button 
          @click="logout" 
          class="bg-gradient-to-r from-red-600 to-red-500 hover:from-red-700 hover:to-red-600 text-white px-16 py-3 rounded-lg font-bold text-lg transition-all duration-300 shadow-md hover:shadow-lg"
        >
          <span class="flex items-center justify-center gap-2">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
            خروج
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

function logout() {
  authStore.logout()
  router.push('/login')
}
</script>

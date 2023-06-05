package com.example.project

import android.content.Context
import android.content.SharedPreferences
import android.util.Log
import androidx.lifecycle.ViewModel

class PacketViewModel : ViewModel() {
    private var p0: String = "-1"   // 목표 단계
    private var p1: String = "OFFAIR"   // 스트리밍 요청
    private var p2: String = "0"        // 전원제어
    private var p3: String = "00"     // 알람시간
    private var p4: String = "00"     // 알람모드

    // 필요한 필드 업데이트 메서드들을 추가합니다.
    fun updateParameter0(value: String) {
        p0 = value
    }

    fun updateParameter1(value: String) {
        p1 = value
    }

    fun updateParameter2(value: String) {
        p2 = value
    }

    fun updateParameter3(value: String) {
        p3 = value
    }

    fun updateParameter4(value: String) {
        p4 = value
    }

    fun logPacketData() {
        Log.d("Packet", "Data: p0=${p0}, p1=${p1}, p2=${p2}, p3=${p3}, p4=${p4}")
    }


    fun getSelectedProfileName(context: Context): String? {
        val sharedPreferences = getSharedPreferences(context)
        return sharedPreferences.getString("selected_profile", null)
    }

    fun getProfileJson(context: Context, profileName: String): String? {
        val sharedPreferences = getSharedPreferences(context)
        return sharedPreferences.getString(profileName, null)
    }

    fun saveProfile(context: Context, profile: Profile) {
        val sharedPreferences = getSharedPreferences(context)
        with(sharedPreferences.edit()) {
            putString(profile.name, profile.toJson())
            apply()
        }
    }

    private fun getSharedPreferences(context: Context): SharedPreferences {
        return context.getSharedPreferences(PROFILE_PREFS_KEY, Context.MODE_PRIVATE)
    }

    companion object {
        private const val PROFILE_PREFS_KEY = "profile_prefs_key"
    }
}
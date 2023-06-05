package com.example.project

import android.content.Context
import android.content.SharedPreferences
import android.util.Log
import androidx.lifecycle.ViewModel
import org.json.JSONObject

class PacketViewModel : ViewModel() {
    private var p0: String = "-1"   // 목표 단계
    private var p1: String = "0"   // 스트리밍 요청
    private var p2: String = "0"        // 전원제어
    private var p3: String = "0"     // 알람시간
    private var p4: String = "0"     // 알람모드

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

    fun parsingPacket(packet: ByteArray): JSONObject? {
        val (headerSize, packetBody) = checkingHeader(packet)


        if (headerSize == -1) {
            return null
        }

        return try {
            JSONObject(packetBody)
        } catch (e: Exception) {
            null
        }
    }

    fun makePacketToSend(): Pair<Boolean, ByteArray> {
        val jsonObject = JSONObject()
        jsonObject.put("p0", p0)
        jsonObject.put("p1", p1)
        jsonObject.put("p2", p2)
        jsonObject.put("p3", p3)
        jsonObject.put("p4", p4)

        val packetBody = jsonObject.toString()
        val bodySize = packetBody.length

        val packetHeader = "H:$bodySize"

        val dataToSend = "$packetHeader\r\n$packetBody\r\n\r\n".toByteArray(Charsets.UTF_8)
        Log.d("dataToSend", "$packetHeader\r\n$packetBody\r\n\r\n")


        return true to dataToSend
    }

    fun checkingHeader(packet: ByteArray): Pair<Int, String?> {
        val packetString = packet.decodeToString()
        val lines = packetString.lines()
//        Log.d("lines", "$lines")

        val firstLine = lines.first()
        val headerSize = firstLine.length
        val bodySizeString = firstLine.substringAfter(":")
        val bodySize = bodySizeString.toIntOrNull()

        if (bodySize != null) {
            val body = packetString.substring(headerSize, headerSize + bodySize + 2)
            val endLine = lines.last()
            return if (endLine == "") {
                headerSize to body
            } else {
                -1 to null
            }
        }

        return -1 to null
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
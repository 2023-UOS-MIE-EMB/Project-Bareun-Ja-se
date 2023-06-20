package com.example.project

import android.content.Context
import android.content.SharedPreferences
import android.util.Log
import androidx.lifecycle.ViewModel
import org.json.JSONObject

// 기능 : PacketViewModel이라는 ViewModel 클래스를 정의.  패킷 데이터 관련 작업과 프로필 데이터 관련 작업을 수행하는 메서드들을 제공
class PacketViewModel : ViewModel() {
    private var p0: String = "-1"   // 목표 단계
    private var p1: String = "0"   // 스트리밍 요청
    private var p2: String = "0"        // 전원제어
    private var p3: String = "0"     // 알람시간
    private var p4: String = "0"     // 알람모드

    // 1. 패킷 데이터 관련 메서드

    // 필요한 필드 업데이트 메서드
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

    // 기능 : 패킷을 파싱하여 JSONObject로 반환하는 메서드
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
    // 기능 : 패킷을 생성하여 전송할 준비를 하는 메서드
    fun makePacketToSend(): Pair<Boolean, ByteArray> {
        val jsonObject = JSONObject()
        jsonObject.put("0", p0)
        jsonObject.put("1", p1)
        jsonObject.put("2", p2)
        jsonObject.put("3", p3)
        jsonObject.put("4", p4)

        val packetBody = jsonObject.toString()
        val bodySize = packetBody.length

        val packetHeader = "H:$bodySize"

        val dataToSend = "$packetHeader\r\n$packetBody\r\n\r\n".toByteArray(Charsets.UTF_8)
        //Log.d("dataToSend", "$packetHeader\r\n$packetBody\r\n\r\n")


        return true to dataToSend
    }
    // 기능 : 패킷의 헤더를 확인하고 헤더 크기와 바디를 반환하는 메서드
    fun checkingHeader(packet: ByteArray): Pair<Int, String?> {
        val packetString = packet.decodeToString()
        val lines = packetString.lines()

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

    // 2. 프로필필 데이 관련 메서드

    // 기능 : 선택된 프로필 이름을 가져오는 메서드
    fun getSelectedProfileName(context: Context): String? {
        val sharedPreferences = getSharedPreferences(context)
        return sharedPreferences.getString("selected_profile", null)
    }

    // 기능 : 주어진 프로필 이름에 해당하는 프로필 JSON 데이터를 가져오는 메서드
    fun getProfileJson(context: Context, profileName: String): String? {
        val sharedPreferences = getSharedPreferences(context)
        return sharedPreferences.getString(profileName, null)
    }

    // 기능 : 주어진 프로필 객체를 JSON으로 직렬화하여 SharedPreferences에 저장하는 메서드
    fun saveProfile(context: Context, profile: Profile) {
        val sharedPreferences = getSharedPreferences(context)
        with(sharedPreferences.edit()) {
            putString(profile.name, profile.toJson())
            apply()
        }
    }
    // 기능 : SharedPreferences 인스턴스를 가져오는 메서드
    private fun getSharedPreferences(context: Context): SharedPreferences {
        return context.getSharedPreferences(PROFILE_PREFS_KEY, Context.MODE_PRIVATE)
    }
    // 위의 함수 사용하기 위해 필요한 인자
    companion object {
        private const val PROFILE_PREFS_KEY = "profile_prefs_key"
    }
}
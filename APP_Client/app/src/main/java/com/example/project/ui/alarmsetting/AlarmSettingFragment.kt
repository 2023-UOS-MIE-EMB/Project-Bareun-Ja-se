package com.example.project.ui.alarmsetting

import NetworkManager
import android.content.Context
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.Switch
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.fragment.findNavController
import com.example.project.PacketViewModel
import com.example.project.Profile
import com.example.project.R

// 기능 : 사용자가 알람을 설정하고 저장할 수 있는 기능을 제공하는 프래그먼트
class AlarmSettingFragment : Fragment() {

    private lateinit var packetViewModel: PacketViewModel
    private val networkManager = NetworkManager()


    private var selectedAlarmMode: String? = null
    private var isAlarmOn: Boolean = false

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_alarmsetting, container, false)

        packetViewModel = ViewModelProvider(requireActivity()).get(PacketViewModel::class.java)

        val profileAlarmTimeEditText = view.findViewById<EditText>(R.id.profileAlarmTimeEditText)

        val alarmSwitch = view.findViewById<Switch>(R.id.alarmSwitch)
        val alarmSoundmodeButton = view.findViewById<Button>(R.id.alarmSoundmodeButton)
        val alarmVibemodeButton = view.findViewById<Button>(R.id.alarmVibemodeButton)
        val saveButton = view.findViewById<Button>(R.id.saveAlarmSettingButton)

        profileAlarmTimeEditText.isEnabled = false
        alarmSwitch.isChecked = false
        alarmSoundmodeButton.isEnabled = false
        alarmVibemodeButton.isEnabled = false

        // 기능 : 사용자가 알람을 켜거나 끌 수 있는 스위치 제공
        alarmSwitch.setOnCheckedChangeListener { _, isChecked ->
            isAlarmOn = isChecked
            if (isChecked) {
                profileAlarmTimeEditText.isEnabled = true
                alarmSoundmodeButton.isEnabled = true
                alarmVibemodeButton.isEnabled = true
                Toast.makeText(requireContext(), "알람 ON", Toast.LENGTH_SHORT).show()
            } else {
                profileAlarmTimeEditText.isEnabled = false
                alarmSoundmodeButton.isEnabled = false
                alarmVibemodeButton.isEnabled = false
                Toast.makeText(requireContext(), "알람 OFF", Toast.LENGTH_SHORT).show()
            }
        }

        alarmVibemodeButton.setOnClickListener { selectAlarmMode("진동") }     //진동
        alarmSoundmodeButton.setOnClickListener { selectAlarmMode("소리") }    //소리

        // 기능 : 알람 설정을 프로필에 저장한 후 패킷을 보내는 버튼
        saveButton.setOnClickListener {
            val sharedPreferences =
                requireContext().getSharedPreferences(PROFILE_PREFS_KEY, Context.MODE_PRIVATE)
            val selectedProfileName = sharedPreferences.getString("selected_profile", null)
            if (selectedProfileName != null) {
                val profileJson = sharedPreferences.getString(selectedProfileName, null)
                if (profileJson != null) {
                    var profile = Profile.fromJson(profileJson)
                    profile?.let {
                        it.alarmMode = selectedAlarmMode ?: "미설정"
                        it.alarmTime = if (profileAlarmTimeEditText.text.toString().isNotBlank()) {
                            profileAlarmTimeEditText.text.toString()
                        } else {
                            "미설정"
                        }
                        saveProfile(requireContext(), it)
                        Toast.makeText(requireContext(), "알람 설정이 저장되었습니다.", Toast.LENGTH_SHORT)
                            .show()
                        if (it.alarmTime == "미설정") {
                            packetViewModel.updateParameter3("0")
                        } else {
                            packetViewModel.updateParameter3(it.alarmTime)
                        }
                        if (it.alarmMode == "진동") {
                            packetViewModel.updateParameter4("1")
                        } else if (it.alarmMode == "소리") {
                            packetViewModel.updateParameter4("2")
                        } else if (it.alarmMode == "미설정") {
                            packetViewModel.updateParameter4("0")
                        }
                        var resultPacket: Pair<Boolean, ByteArray> = packetViewModel.makePacketToSend()
                        val isSuccess: Boolean = resultPacket.first
                        val dataToSend: ByteArray = resultPacket.second
                        Log.d("Packet", "Data: ${packetViewModel.parsingPacket(dataToSend)}")

                        if (isSuccess) {
                            networkManager.sendPacketToServer(dataToSend, packetViewModel, requireContext())
                        } else {
                            Toast.makeText(requireContext(), "패킷 생성 실패", Toast.LENGTH_SHORT).show()
                        }
                        findNavController().navigateUp()
                    }
                }
            }
        }

        return view
    }

    private fun selectAlarmMode(alarmMode: String) {
        selectedAlarmMode = alarmMode
        Toast.makeText(requireContext(), "선택된 알람 모드: $alarmMode", Toast.LENGTH_SHORT).show()
    }

    companion object {
        const val PROFILE_PREFS_KEY = "profile_prefs_key"

        fun saveProfile(context: Context, profile: Profile) {
            val sharedPreferences = context.getSharedPreferences(PROFILE_PREFS_KEY, Context.MODE_PRIVATE)
            with(sharedPreferences.edit()) {
                putString(profile.name, profile.toJson())
                commit()
            }
        }
    }
}

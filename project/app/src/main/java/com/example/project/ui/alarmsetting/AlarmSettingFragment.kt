package com.example.project.ui.alarmsetting

import android.content.Context
import android.content.SharedPreferences
import android.os.Bundle
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

class AlarmSettingFragment : Fragment() {

    private lateinit var packetViewModel: PacketViewModel

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
        val alarmSoundvibemodeButton = view.findViewById<Button>(R.id.alarmSoundvibemodeButton)
        val saveButton = view.findViewById<Button>(R.id.saveAlarmSettingButton)

        profileAlarmTimeEditText.isEnabled = false
        alarmSwitch.isChecked = false
        alarmSoundmodeButton.isEnabled = false
        alarmVibemodeButton.isEnabled = false
        alarmSoundvibemodeButton.isEnabled = false

        alarmSwitch.setOnCheckedChangeListener { _, isChecked ->
            isAlarmOn = isChecked
            if (isChecked) {
                profileAlarmTimeEditText.isEnabled = true
                alarmSoundmodeButton.isEnabled = true
                alarmVibemodeButton.isEnabled = true
                alarmSoundvibemodeButton.isEnabled = true
                Toast.makeText(requireContext(), "알람 ON", Toast.LENGTH_SHORT).show()
            } else {
                profileAlarmTimeEditText.isEnabled = false
                alarmSoundmodeButton.isEnabled = false
                alarmVibemodeButton.isEnabled = false
                alarmSoundvibemodeButton.isEnabled = false
                Toast.makeText(requireContext(), "알람 OFF", Toast.LENGTH_SHORT).show()
            }
        }

        alarmSoundmodeButton.setOnClickListener { selectAlarmMode("소리") }
        alarmVibemodeButton.setOnClickListener { selectAlarmMode("진동") }
        alarmSoundvibemodeButton.setOnClickListener { selectAlarmMode("소리 / 진동") }

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
                        packetViewModel.updateParameter3(it.alarmTime)  // 알람 시간 패킷 인자로 할당
                        packetViewModel.updateParameter4(it.alarmMode)
                        packetViewModel.logPacketData()
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

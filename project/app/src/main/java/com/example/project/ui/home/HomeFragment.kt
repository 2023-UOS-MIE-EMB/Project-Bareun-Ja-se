package com.example.project.ui.home

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.net.ConnectivityManager
import android.net.Network
import android.net.NetworkCapabilities
import android.net.NetworkRequest
import android.net.wifi.WifiConfiguration
import android.net.wifi.WifiManager
import android.net.wifi.WifiNetworkSpecifier
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import androidx.core.app.ActivityCompat
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.fragment.findNavController
import com.example.project.PacketViewModel
import com.example.project.Profile
import com.example.project.R
import com.example.project.databinding.FragmentHomeBinding
import com.example.project.ui.addprofile.AddProfileFragment.Companion.PROFILE_PREFS_KEY



class HomeFragment : Fragment() {

    private lateinit var packetViewModel: PacketViewModel

    private var _binding: FragmentHomeBinding? = null
    private val binding get() = _binding!!

    private lateinit var profileNameTextView: TextView
    private lateinit var profileStepTextView: TextView
    private lateinit var profileTimeTextView: TextView
    private lateinit var profileAlarmTextView: TextView


    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        _binding = FragmentHomeBinding.inflate(inflater, container, false)
        val view = binding.root


        // Initialize the views
        profileNameTextView = view.findViewById(R.id.profile_name)
        profileStepTextView = view.findViewById(R.id.profile_step)
        profileTimeTextView = view.findViewById(R.id.profile_time)
        profileAlarmTextView = view.findViewById(R.id.profile_alarm)


        return view
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        packetViewModel = ViewModelProvider(requireActivity()).get(PacketViewModel::class.java)



        val sharedPreferences = requireContext().getSharedPreferences(PROFILE_PREFS_KEY, Context.MODE_PRIVATE)
        val selectedProfileName = sharedPreferences.getString("selected_profile", null)
        if (selectedProfileName != null) {
            val profileJson = sharedPreferences.getString(selectedProfileName, null)
            if (profileJson != null) {
                val selectedProfile = Profile.fromJson(profileJson)
                showProfileDetails(selectedProfile)
            } else {
                Toast.makeText(requireContext(), "프로필이 없습니다. 프로필을 추가해주세요.", Toast.LENGTH_SHORT).show()
                findNavController().navigate(R.id.action_homeFragment_to_addProfileFragment)
            }
        } else {
            Toast.makeText(requireContext(), "프로필이 없습니다. 프로필을 추가해주세요.", Toast.LENGTH_SHORT).show()
            findNavController().navigate(R.id.action_homeFragment_to_addProfileFragment)
        }

        binding.addProfileButton.setOnClickListener {
            findNavController().navigate(R.id.action_homeFragment_to_addProfileFragment)
        }

        binding.changeButton.setOnClickListener {
            findNavController().navigate(R.id.action_homeFragment_to_profileListFragment)
        }

        binding.cameraOuputButton.setOnClickListener {
            packetViewModel.updateParameter1("1")
            packetViewModel.logPacketData()
        }

        binding.trunOffButton.setOnClickListener {
            packetViewModel.updateParameter2("1")
            packetViewModel.logPacketData()
            var resultPacket: Pair<Boolean, ByteArray> = packetViewModel.makePacketToSend()
            val isSuccess: Boolean = resultPacket.first
            val dataToSend: ByteArray = resultPacket.second
            Log.d("Packet", "Data: ${packetViewModel.parsingPacket(dataToSend)}")

        }

        connectToRaspberryPiHotspot(requireContext())


    }


        private fun connectToRaspberryPiHotspot(context: Context) {
        val ssid = "rpi44" // 라즈베리파이 핫스팟의 SSID를 입력합니다.
        val password = "raspberry" // 라즈베리파이 핫스팟의 비밀번호를 입력합니다.

        val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager

        val specifierBuilder = WifiNetworkSpecifier.Builder()
            .setSsid(ssid)

        if (password.isEmpty()) {
            specifierBuilder.setWpa2Passphrase("") // 비밀번호 없는 연결 설정
        } else {
            if (isWpa3Supported(context)) {
                specifierBuilder.setWpa3Passphrase(password)
            } else {
                specifierBuilder.setWpa2Passphrase(password)
            }
        }

        val specifier = specifierBuilder.build()

        val request = NetworkRequest.Builder()
            .addTransportType(NetworkCapabilities.TRANSPORT_WIFI)
            .setNetworkSpecifier(specifier)
            .build()

        val networkCallback = object : ConnectivityManager.NetworkCallback() {
            override fun onAvailable(network: Network) {
                super.onAvailable(network)

                // Wi-Fi에 성공적으로 연결되었을 때
                requireActivity().runOnUiThread {
                    Toast.makeText(context, "라즈베리파이 핫스팟에 연결되었습니다.", Toast.LENGTH_SHORT).show()

                    val sharedPreferences =
                        context.getSharedPreferences(PROFILE_PREFS_KEY, Context.MODE_PRIVATE)
                    val selectedProfileName = sharedPreferences.getString("selected_profile", null)
                    if (selectedProfileName != null) {
                        val profileJson = sharedPreferences.getString(selectedProfileName, null)
                        if (profileJson != null) {
                            val selectedProfile = Profile.fromJson(profileJson)
                            showProfileDetails(selectedProfile)
                        }
                    }
                }
            }
            override fun onUnavailable() {
                super.onUnavailable()
                // Wi-Fi 연결이 불가능한 경우
                requireActivity().runOnUiThread {
                    Toast.makeText(context, "라즈베리파이 핫스팟 연결에 실패했습니다.", Toast.LENGTH_SHORT).show()
                }
            }
        }

        connectivityManager.requestNetwork(request, networkCallback)
    }

    private fun isWpa3Supported(context: Context): Boolean {
        val wifiManager = context.getSystemService(Context.WIFI_SERVICE) as WifiManager
        val wifiInfo = wifiManager.connectionInfo
        val frequency = wifiInfo?.frequency

        // 주파수를 통해 WPA3 지원 여부를 간접적으로 확인
        // 6GHz 대역 (WiFi 6E)을 사용하는 경우 WPA3를 지원한다고 가정
        return frequency != null && frequency >= 5945
    }

    fun showProfileDetails(profile: Profile?) {
        profile?.let {
            profileNameTextView.text = it.name
            profileStepTextView.text = "최적 단계: ${it.optimalStep}"
            profileTimeTextView.text = "알람 시간(분): ${it.alarmTime}"
            profileAlarmTextView.text = "알람 방식: ${it.alarmMode}"
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}


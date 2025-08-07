import subprocess   
from program.common import convert_to_readable , cipher_algorithm_mapping_name, integrity_algorithm_mapping_name, get_tshark_output , security_header_mapping_name, prompt_creator 
from program.openai import openai_response
from program.gemini import gemini_response
from program.deepseek import deepseek_response

def configuration_update_command_factor_retrieve_text(uplink_command, downlink_command, key_estbl_status, message_encoding_type, pcap_file_path, dl_com_invoke_line):
    pcap_file = pcap_file_path

    security_header_field = 'nas_5gs.security_header_type'
    header = get_tshark_output(pcap_file, security_header_field, dl_com_invoke_line)

    first_part = None  # Initialize first_part outside the if statement

    if key_estbl_status:
        key_estbl_status_str = 'Completed'
    else:
        key_estbl_status_str = 'Not completed yet'

    readable_uplink = convert_to_readable(uplink_command)
    readable_uplink = ("initial registration request" if readable_uplink == "registration request" else readable_uplink)      
        

    factor_text = (
        '5G-AKA: ' + key_estbl_status_str + '\n' +
        'Uplink message from the UE: ' + readable_uplink  + '\n' +
        'Subsequent Downlink message from the AMF: ' + convert_to_readable(downlink_command) + '\n' +
        'The downlink message from the AMF was sent as: ' + message_encoding_type + '\n'
    )

    if header is not None and header.strip():
        parts = header.split(',') 

        if parts:  # Check if parts is not empty before accessing its elements
            first_part = parts[0]
            
            name = security_header_mapping_name(str(first_part))

            factor_text += 'Security header: ' + name+ '\n'

    return factor_text
    
    
    
def configuration_update_command_part(factor_to_consider, uplink_command, downlink_command ,response, pcap_file_path,dl_com_invoke_line, renamed_pcap_text,llm_type):
    key_estbl_status = factor_to_consider[0]
    message_encoding_type = factor_to_consider[1]  
    factor_text = configuration_update_command_factor_retrieve_text(uplink_command, downlink_command, key_estbl_status, message_encoding_type,pcap_file_path,dl_com_invoke_line)
    full_prompt = prompt_creator(downlink_command, uplink_command,response,factor_text, renamed_pcap_text)
    
    if llm_type == "openai":
        openai_answer, status = openai_response(full_prompt)
        return full_prompt, openai_answer, status
    elif llm_type == "gemini":
        gemini_answer, status = gemini_response(full_prompt)
        return full_prompt, gemini_answer, status
    elif llm_type == "deepseek":
        deepseek_answer, status = deepseek_response(full_prompt)
        return full_prompt, deepseek_answer, status 
    else:
        raise ValueError(f"Invalid llm_type: {llm_type}. Expected 'openai' or 'gemini' or 'deepseek'.")
        return None, None, None

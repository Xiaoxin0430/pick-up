import requests

def get_city_weather(city: str):
    # api端点，请求json格式数据
    url = f"https://wttr.in/{city}?format=j1"

    try:
        # 发起网络请求
        response = requests.get(url)
        # 检查响应状态
        response.raise_for_status()
        # 解析json数据
        data = response.json()
        
        # 提取天气状态,按照输出选择需要的数据
        current_condition = data['data']['current_condition'][0]
        weather_desc = current_condition['weatherDesc'][0]['value']
        temp_c = current_condition['temp_C']

        return f"{city}当前天气:{weather_desc},温度:{temp_c}"
    except requests.exceptions.RequestException as e:
        return (f"Error查询天气时遇到网络问题: {e}")
    except (KeyError, IndexError) as e:
        return (f"Error解析天气数据时遇到问题: {e}")



if __name__ == "__main__":
    response = get_city_weather("西安")
    print(response)

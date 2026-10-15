import os
from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# 버블 정렬 알고리즘 (단계별 기록 포함)
def bubble_sort_with_steps(arr):
    """
    버블 정렬을 수행하고 각 단계의 배열 상태를 기록합니다.
    Args:
        arr (list): 정렬되지 않은 숫자 리스트.
    Returns:
        tuple: (정렬된 리스트, 단계별 기록 리스트).
    """
    data = arr.copy()
    n = len(data)
    steps = []  # 각 단계별 배열 상태를 저장할 리스트
    
    # 초기 상태 저장
    steps.append({'array': data.copy(), 'compare': [-1, -1], 'swap': [-1, -1]})

    if n == 0:
        return [], steps

    for i in range(n):
        # 마지막 i개 요소는 이미 제자리에 있으므로 제외
        for j in range(0, n - i - 1):
            # 현재 비교 중인 인덱스 저장
            compare_indices = [j, j + 1]
            swap_indices = [-1, -1]
            
            # 인접한 두 요소 비교
            if data[j] > data[j + 1]:
                # 값 교환 (Swap)
                data[j], data[j + 1] = data[j + 1], data[j]
                swap_indices = [j, j + 1]
            
            # 현재 단계의 배열 상태와 비교/교환 정보를 기록
            # 깊은 복사(copy())를 사용하여 배열의 스냅샷 저장
            steps.append({
                'array': data.copy(),
                'compare': compare_indices,
                'swap': swap_indices,
                'meta': {'pass': i, 'index_j': j}
            })
            
    # 최종 정렬 완료 상태 저장
    steps.append({'array': data.copy(), 'compare': [-1, -1], 'swap': [-1, -1]})
    return data, steps

# 시간 복잡도 정보
COMPLEXITY_INFO = {
    "time_complexity_best": "O(n)",
    "time_complexity_avg": "O(n^2)",
    "time_complexity_worst": "O(n^2)",
    "space_complexity": "O(1) - 제자리 정렬(In-place sort) 기준. 본 구현체는 단계 기록으로 인해 O(n^2) 추가 공간 사용."
}

@app.route('/sort', methods=['POST'])
def sort_array():
    """
    POST 요청을 받아 버블 정렬을 수행하는 API 엔드포인트.
    """
    try:
        # 요청 본문(Body)에서 JSON 데이터 파싱
        content = request.json
        if not content or 'data' not in content:
            return jsonify({'error': 'Invalid input. "data" field is required.'}), 400
        
        input_array = content['data']
        
        # 입력 데이터 유효성 검사 (숫자 리스트인지 확인)
        if not isinstance(input_array, list) or not all(isinstance(x, (int, float)) for x in input_array):
            return jsonify({'error': 'Input data must be a list of numbers.'}), 400

        # 버블 정렬 실행 및 단계 기록 생성 (시뮬레이션 지연 추가)
        # time.sleep(0.1) # 서버 동작 상태 확인을 위한 인위적 지연
        sorted_arr, sort_steps = bubble_sort_with_steps(input_array)
        
        # 결과 응답 구성 (정렬된 결과, 단계 기록, 복잡도 정보)
        response_data = {
            'sorted_array': sorted_arr,
            'steps': sort_steps,
            'total_steps': len(sort_steps),
            'complexity': COMPLEXITY_INFO,
            'status': 'success'
        }
        return jsonify(response_data)

    except Exception as e:
        # 예외 발생 시 에러 메시지 반환
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def health_check():
    """간단한 상태 확인 엔드포인트."""
    return "Bubble Sort Server is running.", 200

if __name__ == '__main__':
    # 포트 설정 (Cloud Run은 PORT 환경 변수를 사용)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

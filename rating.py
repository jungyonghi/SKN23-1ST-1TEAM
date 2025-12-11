import streamlit as st
import pandas as pd

def rating(data):
    from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

    df = pd.DataFrame(data)

    # 🔥 carGradeNbr를 유지 (숨김 처리)
    df = df[['carGradeNbr', 'carGradeNm', 'gradeUsedCarPrice']]
    
    # 라디오 컬럼 추가
    df.insert(0, " ", "")

    # 가격 렌더링 스타일
    price_style = JsCode("""
    function(params) {
        return {
            'color': '#B22222',
            'font-weight': 'bold',
            'text-align': 'right'
        }
    };
    """)

    # 라디오 버튼 렌더러 (초기 선택 상태 추가)
    radio_renderer = JsCode("""
    class RadioRenderer {
      init(params) {
        this.params = params;
        this.eGui = document.createElement('input');
        this.eGui.type = 'radio';
        this.eGui.name = 'row_select';
        
        // 첫 번째 행은 기본 선택
        if (params.node.rowIndex === 0) {
          this.eGui.checked = true;
        }
        
        this.eGui.addEventListener('change', () => {
          params.api.forEachNode(node => { node.setSelected(false); });
          params.node.setSelected(true);
        });
      }
      getGui() {
        return this.eGui;
      }
    }
    """)

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection("single", pre_selected_rows=[0])  # 첫 번째 행 사전 선택
    gb.configure_column(" ", headerName=" ", width=60, cellRenderer=radio_renderer)
    gb.configure_column("carGradeNbr", hide=True)  # carGradeNbr 숨김 처리
    gb.configure_column("gradeUsedCarPrice", cellStyle=price_style)

    grid_options = gb.build()

    grid_res = AgGrid(
        df,
        gridOptions=grid_options,
        allow_unsafe_jscode=True,
        update_mode="MODEL_CHANGED",
        fit_columns_on_grid_load=True,
        data_return_mode='FILTERED_AND_SORTED',
    )

    selected = grid_res.get("selected_rows", [])

    # DataFrame → dict 변환
    if hasattr(selected, "to_dict"):
        selected = selected.to_dict("records")

    # 선택된 값이 없으면 0번 행을 기본값으로 설정
    if not selected and len(df) > 0:
        selected = [df.iloc[0].to_dict()]

    # 🎉 선택된 carGradeNbr 반환
    selected_id = selected[0].get("carGradeNbr") if selected else None

    return selected_id
# Mindflow 鎶€鏈璁℃枃妗?(绮剧畝鐗?

> **鍩轰簬**: ARCHITECTURE.md v1.0  
> **鐗堟湰**: v1.2  
> **鏃ユ湡**: 2026-01-18  
> **鐘舵€?*: 鏍稿績鏈哄埗宸茬‘瀹?

---

## 馃幆 鏈枃妗ｇ洰鐨?

鏈枃妗ｈˉ鍏?ARCHITECTURE.md,鐢ㄦ祦绋嬪浘鍜屼吉浠ｇ爜璇存槑鏍稿績鏈哄埗銆?

---

## 馃搳 鏁版嵁缁撴瀯澧炲己

### Skill 鑺傜偣鏂板瀛楁

```
Skill {
    ... (鍩虹瀛楁瑙?ARCHITECTURE.md)
    
    # 鏂板: 瑙勫垝鐩稿叧
    preconditions: ["has_csv_file"]      # 鍓嶇疆鏉′欢
    effects: ["has_dataframe"]           # 浜х敓鏁堟灉
    
    # 鏂板: 鏂规硶璁鸿瘎鍒?
    methodology_scores: {
        "meth_simple": 0.9,              # 瀵瑰悇鏂规硶璁虹殑绗﹀悎搴?0-1
        "meth_stdlib": 0.7
    }
}
```

### Methodology 鑺傜偣鏂板瀛楁

```
Methodology {
    ... (鍩虹瀛楁瑙?ARCHITECTURE.md)
    
    # 鏂板: 璇勪及瑙勫垯
    evaluation_rule: "妫€鏌ユ槸鍚︿娇鐢ㄦ爣鍑嗗簱"  # 鏂囨湰鎻忚堪鎴栦唬鐮?
    weight: 0.8                           # 鍏ㄥ眬鏉冮噸 0-1
}
```

## 馃敆 Skills 璋冪敤鏂瑰紡 (娣峰悎妯″紡)

### 鏁版嵁缁撴瀯

```
Skill {
    name: "鏁版嵁娓呮礂娴佺▼"
    instructions: """
    1. 璇诲彇CSV鏂囦欢
    2. 楠岃瘉鏁版嵁瀹屾暣鎬?
    3. 澶勭悊缂哄け鍊?
    4. 杈撳嚭娓呮礂鍚庣殑鏁版嵁
    """
    called_skills: ["CSV澶勭悊", "鏁版嵁楠岃瘉"]  # 澹版槑渚濊禆
}
```

### 鎵ц娴佺▼

```
婵€娲?Skill
    鈫?
LLM 璇诲彇 instructions
    鈫?
閫愭鎵ц:
  鈹溾攢 璇嗗埆闇€瑕佽皟鐢ㄧ殑瀛?Skill
  鈹溾攢 浠?called_skills 涓煡鎵?
  鈹溾攢 璋冪敤骞朵紶閫掓暟鎹?
  鈹斺攢 缁х画涓嬩竴姝?
    鈫?
瀹屾垚
```

### 鍏抽敭璁捐

**called_skills 鐨勪綔鐢?*:
- 澹版槑渚濊禆(鐢ㄤ簬瑙勫垝)
- 闄愬埗璋冪敤鑼冨洿(瀹夊叏鎬?
- 寤虹珛鍥剧粨鏋勫叧鑱?

**LLM 鐨勮亴璐?*:
- 鐞嗚В instructions
- 鍐冲畾璋冪敤鏃舵満
- 澶勭悊鏁版嵁浼犻€?

**瀹炵幇浼唬鐮?*:
```python
def execute_skill(skill, context):
    prompt = f"""
    Skill: {skill.name}
    姝ラ: {skill.instructions}
    鍙敤瀛怱kills: {skill.called_skills}
    褰撳墠鐘舵€? {context}
    """
    return llm.execute_with_tools(prompt, tools=skill.called_skills)
```


---

## 馃攳 鏂规硶璁鸿瘎鍒嗘満鍒?

### 娴佺▼鍥?

```
鐢ㄦ埛璇锋眰
    鈫?
鍚戦噺鎼滅储 鈫?鍊欓€?Skills [A, B, C]
    鈫?
瀵规瘡涓?Skill:
    鈹溾攢 鑾峰彇 methodology_scores
    鈹溾攢 鍔犳潈姹傚拰: 危(鏂规硶璁烘潈閲?脳 绗﹀悎搴?
    鈹溾攢 褰掍竴鍖? 鎬诲拰 / 鎬绘潈閲?
    鈹斺攢 娣峰悎鍘嗗彶鎴愬姛鐜? 0.7脳璇勫垎 + 0.3脳success_rate
    鈫?
鎺掑簭 鈫?閫夋嫨寰楀垎鏈€楂樼殑 Skill
```

### 浼唬鐮?

```python
def calculate_skill_score(skill, methodologies):
    weighted_sum = 0
    total_weight = 0
    
    for meth in methodologies:
        score = skill.methodology_scores.get(meth.id, 0.5)
        weighted_sum += meth.weight * score
        total_weight += meth.weight
    
    base_score = weighted_sum / total_weight
    
    # 娣峰悎鍘嗗彶琛ㄧ幇
    if skill.usage_count > 0:
        final = 0.7 * base_score + 0.3 * skill.success_rate
    else:
        final = base_score
    
    return clamp(final, 0, 1)
```

---

## 馃攧 Skills 缁勫悎鏈哄埗 (瑙勫垝寮?

### 娴佺▼鍥?

```
鐢ㄦ埛: "澶勭悊CSV骞剁敓鎴愬浘琛?
    鈫?
LLM 瑙ｆ瀽鐩爣 鈫?["has_dataframe", "has_chart"]
    鈫?
褰撳墠鐘舵€? {"has_csv_file"}
    鈫?
瀵规瘡涓洰鏍囩姸鎬?
    鈹溾攢 鎵捐兘浜х敓璇ョ姸鎬佺殑 Skills
    鈹溾攢 鎸夋柟娉曡璇勫垎鎺掑簭
    鈹溾攢 閫夋嫨鏈€浣?Skill
    鈹溾攢 閫掑綊澶勭悊鍓嶇疆鏉′欢
    鈹斺攢 娣诲姞鍒版墽琛岃鍒?
    鈫?
杩斿洖: [Skill("CSV澶勭悊"), Skill("鏁版嵁鍙鍖?)]
```

### 浼唬鐮?

```python
def plan_skills(user_goal, available_skills, current_state):
    # 1. LLM 瑙ｆ瀽鐩爣
    required_effects = llm.parse(user_goal)
    # 渚? ["has_dataframe", "has_chart"]
    
    # 2. 璐績鎼滅储
    plan = []
    state = current_state.copy()
    
    for target in required_effects:
        if target in state:
            continue
        
        # 鎵惧€欓€?Skills
        candidates = [s for s in available_skills if target in s.effects]
        
        # 璇勫垎鎺掑簭
        best = max(candidates, key=lambda s: score(s))
        
        # 閫掑綊澶勭悊鍓嶇疆鏉′欢
        for precond in best.preconditions:
            if precond not in state:
                sub_plan = plan_skills(precond, available_skills, state)
                plan.extend(sub_plan)
        
        plan.append(best)
        state.update(best.effects)
    
    return plan
```

---

## 馃幁 鐢ㄦ埛浜や簰涓夌骇绛栫暐

### 鍐崇瓥娴佺▼

```
鎿嶄綔鍙戠敓
    鈫?
璇勪及椋庨櫓 (0-1)
    鈫?
    鈹溾攢 < 0.3: 闈欓粯鎵ц (涓嶆墦鏂?
    鈹溾攢 0.3-0.8: 鍔犲叆闃熷垪 (浠诲姟瀹屾垚鏃跺睍绀?
    鈹斺攢 > 0.8: 绔嬪嵆纭 (寮圭獥)
```

### 椋庨櫓璇勪及瑙勫垯

```
鎿嶄綔绫诲瀷          鍩虹椋庨櫓    褰卞搷鑼冨洿璋冩暣
鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€
artifact_add      0.1        local: 脳1, global: 脳1.5
skill_update      0.5        local: 脳1, global: 脳1.5
skill_create      0.6        local: 脳1, global: 脳1.5
methodology_change 0.9       local: 脳1, global: 脳1.5
```

### 闃熷垪澶勭悊

```
浠诲姟瀹屾垚鏃?
    鈫?
妫€鏌ラ槦鍒?
    鈹溾攢 楂橀闄?(>0.7): 蹇呴』纭
    鈹斺攢 浣庨闄?(鈮?.7): 鍙€夌‘璁?1灏忔椂鍚庤嚜鍔ㄦ壒鍑?
```

---

## 馃洝锔?閿欒澶勭悊鍜屽閿欐満鍒?

### 鍒嗗眰閿欒澶勭悊

```
L1: LLM 璋冪敤灞?
  鈹溾攢 缃戠粶閿欒 鈫?閲嶈瘯(3娆?鎸囨暟閫€閬?
  鈹溾攢 API 闄愭祦 鈫?绛夊緟 + 闄嶇骇
  鈹溾攢 鍝嶅簲瓒呮椂 鈫?閲嶈瘯 + 缂╃煭 prompt
  鈹斺攢 瑙ｆ瀽閿欒 鈫?璁板綍 + 榛樿鍊?

L2: Skills 鎵ц灞?
  鈹溾攢 Skill 涓嶅瓨鍦?鈫?鎺ㄨ崘鐩镐技 Skills
  鈹溾攢 鍓嶇疆鏉′欢涓嶆弧瓒?鈫?鑷姩婊¤冻 or 鎻愮ず
  鈹溾攢 鎵ц澶辫触 鈫?璁板綍 + 闄嶄綆 success_rate
  鈹斺攢 閮ㄥ垎鎴愬姛 鈫?杩斿洖宸插畬鎴愰儴鍒?

L3: 鐭ヨ瘑搴撳眰
  鈹溾攢 鍥炬煡璇㈠け璐?鈫?闄嶇骇鍒板悜閲忔悳绱?
  鈹溾攢 鍚戦噺鎼滅储澶辫触 鈫?杩斿洖榛樿 Skills
  鈹溾攢 鏁版嵁涓嶄竴鑷?鈫?鑷姩淇 or 鏍囪
  鈹斺攢 绱㈠紩鎹熷潖 鈫?閲嶅缓绱㈠紩
```

### 鏍稿績绛栫暐

**1. LLM 璋冪敤閲嶈瘯**
```python
def call_llm_with_retry(prompt, max_retries=3):
    for i in range(max_retries):
        try:
            return llm.call(prompt)
        except NetworkError:
            time.sleep(2 ** i)  # 鎸囨暟閫€閬?
        except RateLimitError:
            time.sleep(60)
        except TimeoutError:
            prompt = shorten_prompt(prompt)
    return fallback_response()
```

**2. 浼橀泤闄嶇骇**
```
瀹屾暣鍔熻兘 鈫?闄嶇骇鍔熻兘 鈫?鏈€灏忓姛鑳?

绀轰緥:
- 瀹屾暣: LLM 鐞嗚В + Skills 缁勫悎 + 鎵ц
- 闄嶇骇: 瑙勫垯鍖归厤 + 鍗曚釜 Skill + 鎵ц
- 鏈€灏? 鐢ㄦ埛鎵嬪姩閫夋嫨 Skill
```

**3. 閿欒闅旂**
```
鍗曚釜 Skill 澶辫触 鈮?鏁翠釜浠诲姟澶辫触

绛栫暐:
- 璺宠繃澶辫触鐨?Skill
- 缁х画鎵ц鍏朵粬 Skills
- 鏈€鍚庢眹鎬荤粨鏋?
```

### 鐢ㄦ埛鎻愮ず鍘熷垯

```
1. 娓呮櫚: 璇存槑鍙戠敓浜嗕粈涔?
2. 鍙搷浣? 鍛婅瘔鐢ㄦ埛鍙互鍋氫粈涔?
3. 鍙嬪ソ: 涓嶈鎶€鏈湳璇?

绀轰緥:
鉂?"VectorSearchError: Index not found"
鉁?"鎶辨瓑,鎼滅储鍔熻兘鏆傛椂涓嶅彲鐢ㄣ€傛垜浼氱敤鍏朵粬鏂瑰紡甯綘鏌ユ壘銆?
```

### 瀹炵幇浼樺厛绾?

**Phase 1 蹇呴』**:
- LLM 璋冪敤閲嶈瘯鏈哄埗
- Skills 鎵ц閿欒澶勭悊
- 鍩虹閿欒鏃ュ織

**Phase 2 鍙€?*:
- 鐘舵€佹仮澶嶆満鍒?
- 瀹屾暣鐩戞帶鎸囨爣
- 鑷姩鏁版嵁淇

---


## 馃攳 鍏宠仈鏈哄埗鎶€鏈疄鐜?

### 鍚戦噺鎼滅储

```
鍚姩鏃?
    鈹溾攢 鍔犺浇鎵€鏈?Skills 鐨?name + description
    鈹溾攢 鍚戦噺鍖?(sentence-transformers)
    鈹斺攢 寤虹珛绱㈠紩 (Chroma)

鏌ヨ鏃?
    鈹溾攢 鍚戦噺鍖栫敤鎴疯緭鍏?
    鈹溾攢 鎼滅储 Top-K 鐩镐技 Skills
    鈹斺攢 鎸夐渶鍔犺浇瀹屾暣鍐呭
```

**鎶€鏈爤**: Chroma + sentence-transformers (all-MiniLM-L6-v2)

### 涓婁笅鏂囧姞鏉?

```
缁存姢涓婁笅鏂?
    鈹溾攢 recent_topics: 鏈€杩?0涓叧閿瘝
    鈹斺攢 current_project: 褰撳墠椤圭洰

鏌ヨ鏃?
    鈹溾攢 鍚戦噺鎼滅储 鈫?鍊欓€?Skills
    鈹溾攢 妫€鏌ヤ笌涓婁笅鏂囩殑鍖归厤搴?
    鈹斺攢 璋冩暣寰楀垎: base_score + context_boost (鏈€澶?0.5)
```

---

## 馃摑 鎶€鏈爤

### 鏍稿績渚濊禆

```
鍥炬暟鎹簱:
  - Neo4j (鐢熶骇)
  - NetworkX (寮€鍙?娴嬭瘯)

鍚戦噺鎼滅储:
  - chromadb
  - sentence-transformers

LLM:
  - anthropic / openai
```

### 鎬ц兘鎸囨爣

```
鍚戦噺绱㈠紩:
  - 500 Skills 鈫?绱㈠紩澶у皬 < 10MB
  - 鍚姩鏃堕棿 < 2s

鍥炬煡璇?
  - 鍗曡烦鏌ヨ < 50ms
  - 澶氳烦鏌ヨ < 200ms
```


## 馃攷 鏌ヨ娴佺▼璁捐 (娓愯繘寮?

### Phase 1: 鏈€绠€鏂规 (MVP)

```
鐢ㄦ埛杈撳叆
    鈫?
鍚戦噺鎼滅储 鈫?Top-5 Skills
    鈫?
鏂规硶璁鸿瘎鍒?鈫?鎺掑簭
    鈫?
鍐崇瓥:
  鈹溾攢 寰楀垎宸窛 > 0.3: 杩斿洖鏈€浣?
  鈹斺攢 寰楀垎宸窛 < 0.3: 杩斿洖 Top-3 渚涢€夋嫨
```

**鏍稿績鍋囪**: 鍥剧粨鏋勭殑閭昏繎鍏崇郴浼氳嚜鐒朵綋鐜板湪鍚戦噺鐩镐技搴︿腑

**楠岃瘉鎸囨爣**:
- 棣栨鍛戒腑鐜?> 80%
- 鐢ㄦ埛闇€瑕侀€夋嫨鐨勯鐜?< 20%

### Phase 2: 鍙嶉浼樺寲 (鎸夐渶)

```
鐢ㄦ埛鍙嶉 "涓嶆槸杩欎釜"
    鈫?
鍥剧粨鏋勬煡璇?
  鈹溾攢 鎵?sibling skills (鍚屾柟娉曡涓?
  鈹溾攢 鎵?related skills (璋冪敤鍏崇郴)
  鈹斺攢 鎵?upstream/downstream (鍓嶅悗缃?
    鈫?
杩斿洖鏂板€欓€?
```

**瑙﹀彂鏉′欢**:
- 鐢ㄦ埛鏄庣‘鎷掔粷
- 棣栨鎼滅储寰楀垎 < 0.5

**瀹炵幇绛栫暐**: 鍏堝疄鐜?Phase 1,鏍规嵁瀹為檯鏁堟灉鍐冲畾鏄惁闇€瑕?Phase 2

---

## 鉁?鏍稿績鍐崇瓥鎬荤粨

1. **Skills 缁勫悎**: 瑙勫垝寮?(HTN Planning 绠€鍖栫増)
2. **鏂规硶璁洪噺鍖?*: 璇勫垎鏈哄埗 + 褰掍竴鍖?
3. **鐢ㄦ埛浜や簰**: 涓夌骇绛栫暐 (闈欓粯/闃熷垪/绔嬪嵆)
4. **鍚戦噺鎼滅储**: Chroma + sentence-transformers
5. **鍥炬暟鎹簱**: Neo4j(鐢熶骇) / NetworkX(寮€鍙?

---

**鐗堟湰**: v1.2  
**鏈€鍚庢洿鏂?*: 2026-01-18  
**鐘舵€?*: 鏍稿績鏈哄埗宸茬‘瀹?寰呭疄鐜?


---

## 馃尡 鍐峰惎鍔ㄧ瀛愬簱璁捐

### 绮剧畝鏂规 (MVP)

**鏂规硶璁哄眰**: 5涓?
1. 绠€鍗曚紭浜庡鏉?
2. 浼樺厛浣跨敤鏍囧噯搴?鎴愮啛宸ュ叿
3. 淇濇寔涓€鑷存€?
4. 浠庡皬寮€濮?閫愭杩唬
5. 璁板綍鍜屽鐩?

**Skills 灞?*: 15-20涓?

```
鐢熸椿绠＄悊 (6涓?:
鈹溾攢 浠诲姟鍒嗚В
鈹溾攢 浠诲姟璺熻釜
鈹溾攢 鏃ョ▼瑙勫垝
鈹溾攢 绗旇鏁寸悊
鈹溾攢 鏃ュ鐩?
鈹斺攢 鍛ㄥ鐩?

鏁版嵁澶勭悊 (6涓?:
鈹溾攢 CSV 澶勭悊
鈹溾攢 JSON 澶勭悊
鈹溾攢 鏁版嵁娓呮礂
鈹溾攢 鏁版嵁楠岃瘉
鈹溾攢 鏁版嵁杞崲
鈹斺攢 鏁版嵁鍙鍖?

浠ｇ爜杈呭姪 (3涓?:
鈹溾攢 Python 鑴氭湰鐢熸垚
鈹溾攢 鍑芥暟閲嶆瀯
鈹斺攢 閿欒澶勭悊

閫氱敤宸ュ叿 (2涓?:
鈹溾攢 鏂囦欢璇诲啓
鈹斺攢 鍛戒护琛岃皟鐢?
```

**鍓骇鍝佸眰**: 姣忎釜 Skill 1涓牳蹇冨壇浜у搧

### 鐢熸垚鏂瑰紡

- 鐢熸椿绠＄悊绫? 鎵嬪伐缂栧啓(鏍稿績浠峰€?
- 鍏朵粬绫? LLM 鐢熸垚 + 浜哄伐瀹℃牳
- 鍚庣画: 浠?Claude Skills 搴撳弬鑰冧紭鍖?

### 瀹炴柦椤哄簭

**Phase 1 (Week 3)**: 5涓熀纭€ Skills
- 浠诲姟鍒嗚В, CSV澶勭悊, Python鑴氭湰鐢熸垚, 鏂囦欢璇诲啓, 鏃ュ鐩?

**Phase 2 (Week 4)**: 鎵╁睍鍒?15-20涓?

**鍚庣画**: 浠庝娇鐢ㄤ腑瀛︿範,鑷姩鐢熸垚鏂?Skills

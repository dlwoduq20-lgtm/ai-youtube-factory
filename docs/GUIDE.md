# AI YouTube Factory — 로컬 작업 지침서

이 문서는 지금까지의 기획·결정·작업 내용을 정리한 것이다. 로컬 PC에서 이어서 작업할 때 이 문서부터 읽는다.

---

## 1. 지금 어디까지 왔나

| 항목 | 상태 |
|---|---|
| 한국어 만평 쇼츠 엔진 (ep01~ep03) | 완성. 코드로 그린 캐릭터·모션그래픽·TTS·자막 |
| 영어권 채널 방향 | **남녀탐구생활 모티브의 관계 코미디**로 확정 |
| 영어 파일럿 ep04 `Why Hasn't He Texted Back?` | 제작 완료 (`samples/ep04_texted_back.mp4`, 43초). **유머가 약하다는 판단** → 대본은 나중에 다시 씀 |
| 영상 퀄리티 개선 | **AI 그림 + 코드 컷아웃 애니메이션** 방식으로 가기로 함. 캐릭터 시트 이미지 생성 대기 중 |

작업 브랜치: `ccr-2a4f757b-62fzbp` (아직 main 에 병합 안 됨)

---

## 2. 채널 기획 (확정 사항)

### 콘셉트
- 원작: tvN 《롤러코스터》 〈남녀탐구생활〉 — **포맷 아이디어만 참고**. 원작의 제목·대사·영상·음원·캐릭터는 절대 가져오지 않는다.
- 채널명 후보: **Two Different Universes** (1순위), His Brain vs Hers, Same Situation
- 슬로건: **Same Moment, Two Worlds** — 같은 순간을 남녀가 완전히 다르게 해석한다.

### 에피소드 기본 문법 (매번 똑같이 복제하지 말고 변형할 것)
1. **REALITY** — 실제로 벌어진 일
2. **HER VERSION** — 그녀의 해석·상상
3. **HIS VERSION** — 그의 해석·상상
4. **THE TRUTH** — 둘 다 놓친 진짜 이유 (반전)

### 원칙
- 한쪽 성별을 놀리는 결말 금지. **둘 다 착각했다**는 결말이 기본.
- 캐릭터 대사는 최소화, **내레이터 한 명이 상황을 중계** (TTS 감정 연기 문제 회피).
- 설명보다 사건, 웃음은 표정·행동·대비·타이밍으로.
- 고정 캐릭터(남녀 2명)를 계속 쓰고 성격이 이어지게 한다.

### 첫 소재 후보 (영어 제목)
- When She Says "I'm Fine"
- Why Hasn't He Texted Back? (파일럿 제작됨)
- The 3-Hour Text Reply Game
- When Your Crush Likes Your Story
- 이후 친구·직장·가족으로 확장 (The Group Chat Nobody Replies To, When Your Boss Says "Quick Question" 등)

### 운영 전략
1. 쇼츠(30~60초) 10~15편으로 소재 검증 — 조회수보다 **시청 지속률·첫 3초 이탈·댓글·공유**를 본다.
2. 반응 좋은 소재 2~3개를 4~6분 롱폼으로 확장 (쇼츠 이어붙이기 말고 새 갈등 추가).
3. 수익화 기준: 구독자 1,000 + (롱폼 시청 4,000시간/12개월 또는 쇼츠 1,000만 회/90일). 신청 전 공식 YPP 안내 확인.

---

## 3. 대본 작성 지침 (ep04 피드백 반영)

ep04 를 본 결과 **재미없다**는 판단. 원인과 다음 대본의 규칙:

| ep04 문제 | 다음 대본 규칙 |
|---|---|
| 반전(폰 방전)이 뻔함 | 흔한 결말 금지. 예상 밖의 반전을 먼저 정하고 거꾸로 설계 |
| 과잉 반응이 커지지 않음 | **점점 심해지는(escalation) 구조**: 5분 → 15분 → 30분 → 45분마다 더 미쳐감 |
| 펀치라인이 밋밋 ("nvm.") | 마지막 한 방은 그림만 봐도 웃겨야 함 |
| 43초에 웃음 2~3개 | **5초에 한 번은 웃음 포인트** |
| 미국식 잔잔한 공감 유머 | 남녀탐구생활처럼 **과장된 내레이션 + 과장된 리액션** |

escalation 예시 (그녀):
- 5분: 답장 초안 14개를 썼다 지움
- 15분: 친구 3명과 단톡방 긴급회의
- 30분: 그의 인스타 좋아요 기록을 2019년까지 추적
- 45분: 이별 연설문 완성, 거울 앞 리허설

그 사이 그의 화면은 **매번 똑같이** 소파에서 과자 먹는 중 → 반복 대비로 웃음 증폭.

---

## 4. 제작 방식 결정

### 채택: AI 그림 + 코드 컷아웃 애니메이션
- 캐릭터·배경은 ChatGPT/Gemini 이미지 생성으로 고퀄리티로 만든다.
- 캐릭터를 머리·눈·입·팔·몸 조각으로 나눠 Python 코드로 움직인다 (짤툰·사우스파크식 컷아웃).
- 기존 엔진의 TTS·자막·효과음·렌더링 파이프라인은 그대로 재사용 → 자동화 유지, 추가 비용 거의 없음.

### 소리 개선 (그림만큼 중요)
- 남녀탐구생활의 핵심은 내레이터 말투. 무료 Edge TTS → 필요하면 유료 AI 음성(ElevenLabs 등) 또는 원어민 성우(Fiverr 등).
- 코드 합성 효과음 → 무료 효과음 라이브러리로 교체 고려 (상업적 이용 라이선스 확인).

### 제한적 사용: AI 영상 생성 (Kling, Veo 등)
- 비용 + 캐릭터 일관성 문제 → 한 편에 1~2컷, 가장 중요한 장면만.

### 보류: Blender 3D 파이프라인, AI 에이전트 8명 팀
- Blender 3D + 카툰 렌더링: 캐릭터 모델링·얼굴 리그가 자동화 안 되고 몇 달 걸림. "3D 기본 버전 같다"는 문제 재발 위험.
  나중에 전신 동작이 꼭 필요하면 Blender 에서 2D 조각 캐릭터를 뼈대로 움직이는 방식, 걷기·뛰기는 무료 Mixamo 동작 활용을 검토.
- 에이전트 팀: 재미가 검증되기 전엔 과함. 토큰 절약이 필요하면 Claude Code 서브에이전트에 쉬운 작업은 저렴한 모델(Haiku·Sonnet)을 배정하는 정도로 시작.

---

## 5. 캐릭터·배경 이미지 생성 프롬프트

**ChatGPT 이미지 생성에서 같은 대화창 안에서 순서대로** 요청한다 (새 창이면 얼굴이 바뀜). 배경은 반드시 흰색 단색.

**1) 남자 기본**
```
2D flat cartoon character design, clean vector style, thick dark outlines, simple cel shading, like a modern YouTube animated comedy. A man in his late 20s, average guy, messy short dark hair, simple blue hoodie, jeans, sneakers. Full body, front view, standing straight in A-pose with arms slightly away from the body, neutral expression. Plain pure white background, no shadow on the floor, no text. High resolution.
```

**2) 여자 기본**
```
Same art style as the previous image. A woman in her late 20s, shoulder-length brown bob hair, simple pink hoodie, jeans, sneakers. Full body, front view, A-pose with arms slightly away from the body, neutral expression. Plain pure white background, no shadow, no text. High resolution.
```

**3) 표정 시트 (남녀 각각, 여자는 "same woman")**
```
Expression sheet of the same man (same face, same hair, same style). 12 heads only, no body, arranged in a 4x3 grid with lots of space between them, all facing front: neutral, happy, big laugh, smug, suspicious (squinting), angry, shocked (eyes wide), crying, sad, embarrassed (blushing), confused, dead-inside blank stare. Plain pure white background, no text, no labels.
```

**4) 포즈 시트 (남녀 각각)**
```
Pose sheet of the same man, same style. 6 full-body poses spread out with lots of space between them: walking, running, sitting on a couch, looking at a phone with both hands, arms crossed, hands on head in panic. Plain pure white background, no text.
```

**5) 배경 (세로 9:16, 3~4장)**
```
Background art for a 2D cartoon, same flat style, no characters, vertical 9:16. A cozy small apartment living room at night: couch, TV, side table, warm lamp light. Simple shapes, slightly muted colors so characters stand out. No text.
```
`living room` 자리를 `her bedroom with a bed and fairy lights`, `small cafe`, `office desk` 등으로 바꿔 생성.

최소 테스트용: 1~3단계(남녀 기본 + 표정 시트)만 있어도 됨.

### 에셋 저장 규칙 (제안)
```
assets/
  characters/
    him/  base.png  expressions.png  poses.png
    her/  base.png  expressions.png  poses.png
  backgrounds/
    living_room.png  her_bedroom.png  cafe.png  office.png
```
원본 이미지는 그대로 두고, 잘라낸 조각은 `assets/characters/<이름>/parts/` 에 둔다.

---

## 6. 로컬 환경 세팅

```bash
git clone https://github.com/dlwoduq20-lgtm/ai-youtube-factory.git
cd ai-youtube-factory
git checkout ccr-2a4f757b-62fzbp

python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

- **ffmpeg** 별도 설치 필요 (`ffmpeg -version` 으로 확인). Windows 는 winget/choco, Mac 은 `brew install ffmpeg`.
- 폰트는 `assets/fonts/` 에 포함 (Jua, Black Han Sans — 한글·영문 모두 지원).

### 렌더링
```bash
python render.py ep04_texted_back                    # → samples/ep04_texted_back.mp4 (약 2분)
python render.py ep04_texted_back --stills 3,10,20   # 지정 시각 스틸컷 PNG (레이아웃 확인용, 빠름)
```
작업 순서: 스틸컷으로 구도 확인 → 전체 렌더.

### TTS
- 기본: Edge TTS (무료, 인터넷 필요). 영어 내레이터는 `en-GB-RyanNeural`. 다른 후보: `en-US-AndrewNeural`, `en-US-BrianNeural`, `en-GB-ThomasNeural`.
- 순서: edge → google → espeak 자동 폴백. `TTS_BACKEND=edge` 로 강제 가능.
- 결과는 `.cache/tts/` 에 캐시됨 (대본 바꾸면 자동으로 새로 합성).
- Azure Speech 키가 있다면 환경변수(`AZURE_SPEECH_KEY`, `AZURE_SPEECH_REGION`)로만 두고 **절대 커밋하지 않는다**. koreacentral 지역은 Edge 와 같은 음성이라 품질 이득이 없어 현재 미사용.

---

## 7. 코드 구조

```
cartoon_shorts/
  engine.py      이징, 텍스트 캐시, 말풍선·집중선 등 모션그래픽 프리미티브 (1080x1920, 30fps)
  characters.py  ep01 만평 캐릭터
  squire.py      해설 애니메이션 캐릭터(Person)·배경·소품
  explainer.py   대본 기반 에피소드 엔진 (TTS 타임라인, 단어 동기 자막, 립싱크, 믹싱)
  audio.py       BGM·효과음 합성 + 믹싱
  tts.py         TTS 백엔드
  episodes/      에피소드 1개 = 파일 1개
render.py        프레임 → ffmpeg → mp4
```

### 새 에피소드 만드는 법 (ep04 참고)
1. `cartoon_shorts/episodes/epXX_이름.py` 생성
2. `SCRIPT = [(샷이름, [(화자, "대사")], {옵션})]` — `[단어]` 는 노란색 강조
3. 샷마다 `shot_<샷이름>(ctx, lt, sh)` 함수 작성. `sh.m(i)`/`sh.me(i)` = i번째 대사 시작/끝, `sh.word_t(i, k)` = k번째 단어 시각
4. `cues()` 에 효과음 타이밍 (pop, whoosh, stamp, ding, boing, rain, cheer, fall, tick 등)
5. 영어 에피소드는 `Episode(..., cap_chars=14)` (자막 덩어리 길이)
6. 화면 구도: 위 = 상황, 가운데(y≈1300) = 자막, 아래 = 캐릭터 상반신

### ep04 에서 추가된 엔진 기능
- `Episode(cap_chars=...)` — 자막 한 덩어리 최대 글자 수 (한국어 9, 영어 14)
- `Person.draw(prop=함수)` — 손에 든 소품 그리기
- `Person` 포즈 `hold`(폰 들기), `game`(게임패드)

---

## 8. 다음 할 일

1. [ ] **캐릭터 시트 생성** — 5장의 프롬프트로 남녀 기본 + 표정 시트 (최소)
2. [ ] **컷아웃 애니메이션 모듈** `cartoon_shorts/cutout.py` 구현
   - PNG 조각 불러오기 + 흰 배경 제거 (투명화)
   - 조각별 회전 중심(pivot) 설정: 머리·팔·몸통
   - 표정 교체 (표정 시트에서 얼굴 잘라 쓰기), 눈 깜빡임
   - 입 모양: 말할 때 음량에 따라 교체 (기존 `Episode.mouth()` 재사용)
   - 숨쉬기·흔들림 같은 대기 동작, 스쿼시&스트레치, 등장·퇴장 트윈
   - 배경 이미지 + 살짝 패럴랙스 카메라
3. [ ] ep04 의 장면 하나를 새 그림으로 다시 만들어 **기존 vs 새 방식 비교**
4. [ ] escalation 규칙으로 대본 다시 쓰기 (1순위 소재: "I'm Fine" 또는 답장 소재 리메이크)
5. [ ] 내레이터 음성 비교 (Edge 후보 2~3개 vs 유료 음성 샘플)
6. [ ] 쇼츠 공개 → 시청 지속률·댓글 확인 → 다음 소재 결정

---

## 9. 유튜브 정책 주의

- 2025년 7월부터 **대량 생산·반복적 콘텐츠(inauthentic content)** 는 수익화 제한. AI 사용 자체는 괜찮지만 같은 템플릿에 대사만 바꾼 영상은 위험 → 매편 다른 갈등·결말·시각 개그.
- 명백한 애니메이션은 보통 AI 합성 표시 대상이 아니지만, 실제 인물·사건처럼 보이는 합성 장면은 공개 정책 확인.
- 음성·효과음·이미지·폰트의 상업적 이용 권리 확인. 구글 번역 TTS 백엔드는 비공식이라 상업 배포 전 교체.

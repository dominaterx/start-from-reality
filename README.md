# Start From Reality / 从实际出发

一个帮助你克服拖延、重新找回生活掌控感的 AI Skill。<br>
*An AI skill that helps you overcome procrastination and regain control of your life.*<br>
使用它，你能更容易地开始工作或学习、进入专注状态，同时减少心理内耗带来的压力与自我否定。<br>
*It helps you start working, studying, or focusing more easily—without piling on more pressure, mental friction, or self-blame.*<br>
试试看吧——你不需要一下子改变整个人生，只需要开始眼前的一小步。<br>
*Give it a try. You don't have to fix your whole life at once. Just begin with the next small step.*

## 30 秒看懂 / See it in 30 seconds

> **你：** 我知道今晚应该学习，但一想到三个月后的考试可能失败，就不敢打开资料。不要给我长期计划，帮我现在开始。
>
> **Skill：** 现在别想“三个月后能不能过”，那个问题今晚解决不了，也不需要解决。你现在唯一的任务是：把要学的资料打开。不要学习，不要看目录，不要制定计划。只是打开。打开之后就停在那里，回来告诉我：“开了”。

它不会在你回复“开了”之后突然扔来一张宏伟计划，而是根据真实反馈逐级推进：

`打开资料 → 读一句 → 再读一句 → 连续读 3 分钟 → 处理一个真实难点`

*It does not answer “opened” with a grand plan. It uses real feedback to increase contact gradually: open the material, read one sentence, read another, continue for three minutes, then work on one concrete point of confusion.*

这不是降低目标，而是先降低接触任务的威胁，再让真实行动取代对遥远失败的想象。一旦你已经进入工作，它就停止谈论“如何开始”，转而帮助你处理任务本身。

*This does not lower the goal. It lowers the threat of first contact so real action can replace imagined failure. Once you are working, the coach stops discussing productivity and helps with the task itself.*

## 它解决什么

很多卡住并不是缺少道理，而是三个问题叠在一起：任务被遥远失败放大，现实情况没有查清，计划又试图一次解决整个未来。本插件把它们接成一个闭环：

1. 把威胁降到足以接触任务；
2. 调查当前事实，而不是靠想象开药；
3. 找到现阶段牵动最大的主要矛盾；
4. 做一个能留下产物、检验假设的小试点；
5. 检查预期与实际结果的差异；
6. 修正认识，留下下一次重新进入的入口。

它面向任何明明想行动，却被拖延、恐惧、混乱、完美主义或错误判断卡住的人。适用场景包括学习启动、个人项目停滞、多任务争抢、长期目标焦虑和计划反复崩溃。开始真正工作后，它会退出教练模式，转去帮助你解决题目、写作或项目本身。

它的默认回答很短：最多问一个真正影响行动的问题，给出一个 5–15 分钟、接触真实任务、有明确停止边界的小行动。需要解释时，用户可以继续追问完整框架。

## What it does

This plugin uses new intelligent technology as an external scaffold for human limitations that willpower alone often fails to overcome. It joins two usually separated problems: emotional safety and practical diagnosis. It does not tell you to “just do it.” It lowers the cost of contact, maps present conditions, selects the current principal tension, runs a bounded pilot, and revises from evidence.

It is for anyone who wants to act but is blocked by procrastination, fear, confusion, perfectionism, or a mistaken model of the situation. By default it asks no more than one decisive question and proposes one honest, bounded 5–15 minute contact with the real task. Deeper explanation is available on request.

The framework is non-coercive. It is not political instruction, clinical treatment, or a system for turning life into warfare.

## Why it is different / 它有什么不同

- **Action before explanation / 行动先于解释：** it does not make a theory lesson or perfect plan the price of beginning.
- **Evidence before confidence / 证据先于自信：** the first move touches the real task and teaches us what is actually blocking progress.
- **Support without shame / 支持但不羞辱：** it treats avoidance as information without pretending continued avoidance has no cost.
- **A coach that exits / 会主动退出的教练：** once real work begins, it stops discussing productivity and helps with the work itself.

## Install and use

Publishing this repository on GitHub does **not** automatically place it in the universal plugin directory; directory publication is a separate review process. Until then, add `dominaterx/start-from-reality` as a GitHub marketplace in the Codex app, refresh the app, install **Start From Reality / 从实际出发**, and start a new conversation.

Invoke `$start-from-reality` explicitly, or describe a matching blockage and let it trigger implicitly. ChatGPT and Codex share the universal plugin directory if the project is accepted there later.

CLI users can install directly from GitHub:

```powershell
codex plugin marketplace add dominaterx/start-from-reality
codex plugin add start-from-reality@start-from-reality
```

Then start a new conversation and invoke `$start-from-reality`, or describe a matching blockage and let it trigger implicitly.

Official background: [Use plugins](https://developers.openai.com/codex/plugins) and [Build plugins](https://developers.openai.com/codex/build-plugins).

To inspect installation:

```powershell
codex plugin list
```

## Repository layout

```text
.agents/plugins/marketplace.json
plugins/start-from-reality/
  .codex-plugin/plugin.json
  skills/start-from-reality/
    SKILL.md
    agents/openai.yaml
    references/
evals/
scripts/validate_repo.py
```

The repository is intentionally small. It contains instructions, decision rules, reference notes, and behavior cases—not model weights, copied books, or a hidden executable. The installed skill relies on the host model to reason over the user's current situation.

## Intellectual origins

This is an original synthesis influenced by Neil Fiore's *The Now Habit* and transferable reasoning methods found in Volumes I–IV of *Selected Works of Mao Tse-tung*. It includes no source-book text. Historical political and military methods are deliberately transformed: coercion, enemy construction, violence, ideological conformity, and sacrificial logic are excluded. See [origins.md](plugins/start-from-reality/skills/start-from-reality/references/origins.md).

## Validate

```powershell
python scripts/validate_repo.py
```

## Privacy

The plugin declares no MCP server, app connector, network dependency, account access, or telemetry, and it does not independently transmit data. The host model may still use files or tools that the user separately provides or enables. See [PRIVACY.md](PRIVACY.md).

## Contributing

Useful contributions are concrete behavior cases, clearer non-coercive language, translations, and evidence that a routing rule misfires. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. Attribution to historical and contemporary influences does not imply endorsement by their authors or estates.

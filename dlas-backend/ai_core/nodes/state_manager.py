from ai_core.state import GraphState, ProcurementState


class StateManager:

    def run(self, state: GraphState):

        entities = state["entities"]

        procurement = state.get("procurement") or ProcurementState()

        if entities.item is not None:
            procurement.item = entities.item

        if entities.brand is not None:
            procurement.brand = entities.brand

        if entities.quantity is not None:
            procurement.quantity = entities.quantity

        if entities.budget is not None:
            procurement.budget = entities.budget

        if entities.vendor is not None:
            procurement.vendor = entities.vendor

        if entities.delivery_date is not None:
            procurement.delivery_date = entities.delivery_date

        if entities.specifications:

            procurement.specifications.extend(
                entities.specifications
            )

            procurement.specifications = list(
                set(procurement.specifications)
            )

        return {
            "entities": entities,
            "procurement": procurement,
        }